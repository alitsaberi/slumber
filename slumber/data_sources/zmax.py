import logging
import socket

Logger = logging.getLogger("slumber")


class ZmaxSocket:
    def __init__(self, socket: socket.socket):
        """
        Initialise the ZmaxSocket instance with a socket,
        and set default message length.

        Args:
            sock (socket.socket): The socket to use for communication.
        """
        self._msg_len = 4500
        self._server_connected = False
        self.sock = socket

    def connect(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """
        Connect to the specified host and port.

        Args:
            host (str): The host to connect to. Defaults to '127.0.0.1'.
            port (int): The port to connect to. Defaults to 8000.
        """
        try:
            self.sock.connect((host, port))
            self._server_connected = True
        except OSError as msg:
            Logger.error(f"Couldn't connect with the socket-server: {msg}.\n")
            self._server_connected = False

    def send(self, msg: bytes):
        """
        Send a message through the socket.

        Args:
            msg (bytes): The message to send.

        Raises:
            RuntimeError: If the socket connection is broken.
        """
        total_sent = 0
        while total_sent < self._msg_len:
            sent = self.sock.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent = total_sent + sent

    def receive_one_line_buffer(self, type: int = 1) -> bytes | str:
        """
        Receive one line of data from the socket.

        Args:
            type (int): The type of data to return. 0 for binary, 1 for string.

        Returns:
            bytes | str: The received data.

        Raises:
            RuntimeError: If the socket connection is broken.
        """
        chunks = []
        bytes_recd = 0
        while bytes_recd < self._msg_len:
            chunk = self.sock.recv(1)
            if chunk == b"":
                raise RuntimeError("socket connection broken")
            if chunk == b"\r":
                continue
            elif chunk == b"\n":
                break
            else:
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)

        msg = b"".join(chunks)
        # Return binary data
        if type == 0:
            return msg
        # Return decoded string
        else:
            return msg.decode("utf-8")

    def send_string(self, msg: str):
        """
        Send a string message through the socket.

        Args:
            msg (str): The string message to send.
        """
        msg = msg.encode("utf-8")
        self.sock.send(msg)

    def read(self, request_ids: tuple[int] = (0, 1)) -> list[float]:
        """
        Read and process data from the socket.

        Args:
            request_ids (tuple[int]): List of IDs for the requested data.

        Returns:
            list[float]: List of processed data values.
        """
        request_vals = []
        buffer = self.receive_one_line_buffer()

        if str.startswith(buffer, "DEBUG"):  # Ignore debugging messages from server
            pass
        else:
            if str.startswith(buffer, "D"):  # Only process data packets
                p = buffer.split(".")
                if len(p) == 2:
                    buffer = p[1]
                    packet_type = self.get_byte_at(buffer, 0)
                    # Packet type within correct range
                    if (
                        (packet_type >= 1)
                        and (packet_type <= 11)
                        and (len(buffer) == 119)
                    ):
                        # EEG channels
                        eegr = self.get_word_at(buffer, 1)
                        eegl = self.get_word_at(buffer, 3)
                        # Accelerometer channels
                        dx = self.get_word_at(buffer, 5)
                        dy = self.get_word_at(buffer, 7)
                        dz = self.get_word_at(buffer, 9)
                        # PPG channels (not plotted)
                        oxy_ir_ac = self.get_word_at(buffer, 27)
                        oxy_r_ac = self.get_word_at(buffer, 25)
                        oxy_dark_ac = self.get_word_at(buffer, 34)
                        oxy_ir_dc = self.get_word_at(buffer, 17)
                        oxy_r_dc = self.get_word_at(buffer, 15)
                        oxy_dark_dc = self.get_word_at(buffer, 32)
                        # other channels (not plotted)
                        body_temp = self.get_word_at(buffer, 36)
                        nasal_l = self.get_word_at(buffer, 11)
                        nasal_r = self.get_word_at(buffer, 13)
                        light = self.get_word_at(buffer, 21)
                        bat = self.get_word_at(buffer, 23)
                        noise = self.get_word_at(buffer, 19)
                        # convert
                        eegr, eegl = self.scale_eeg(eegr), self.scale_eeg(eegl)
                        dx = self.scale_accel(dx)
                        dy = self.scale_accel(dy)
                        dz = self.scale_accel(dz)
                        body_temp = self.body_temp(body_temp)
                        bat = self.battery_voltage(bat)
                        # for function return
                        result = [
                            eegr,
                            eegl,
                            dx,
                            dy,
                            dz,
                            body_temp,
                            bat,
                            noise,
                            light,
                            nasal_l,
                            nasal_r,
                            oxy_ir_ac,
                            oxy_r_ac,
                            oxy_dark_ac,
                            oxy_ir_dc,
                            oxy_r_dc,
                            oxy_dark_dc,
                        ]
                        for i in request_ids:
                            request_vals.append(result[i])

        return request_vals

    def get_byte_at(self, buffer: str, idx: int = 0) -> int:
        """
        Get a byte from the buffer at the specified index.

        Args:
            buffer (str): The buffer to read from.
            idx (int): The index to read at.

        Returns:
            int: The byte value.
        """
        s = buffer[idx * 3 : idx * 3 + 2]
        return self.hex_to_dec(s)

    def get_word_at(self, buffer: str, idx: int = 0) -> int:
        """
        Get a word (2 bytes) from the buffer at the specified index.

        Args:
            buffer (str): The buffer to read from.
            idx (int): The index to read at.

        Returns:
            int: The word value.
        """
        w = self.get_byte_at(buffer, idx) * 256 + self.get_byte_at(buffer, idx + 1)
        return w

    def scale_eeg(self, e: int) -> float:
        """
        Scale the EEG value.

        Args:
            e (int): The raw EEG value.

        Returns:
            float: The scaled EEG value.
        """
        uv_range = 3952
        d = e - 32768
        d = d * uv_range
        d = d / 65536
        return d

    def scale_accel(self, dx: int) -> float:
        """
        Scale the accelerometer value.

        Args:
            dx (int): The raw accelerometer value.

        Returns:
            float: The scaled accelerometer value.
        """
        d = dx * 4 / 4096 - 2
        return d

    def battery_voltage(self, vbat: int) -> float:
        """
        Convert raw battery value to voltage.

        Args:
            vbat (int): The raw battery value.

        Returns:
            float: The battery voltage.
        """
        v = vbat / 1024 * 6.60
        return v

    def body_temp(self, body_temp: int) -> float:
        """
        Convert raw body temperature value to Celsius.

        Args:
            body_temp (int): The raw body temperature value.

        Returns:
            float: The body temperature in Celsius.
        """
        v = body_temp / 1024 * 3.3
        t = 15 + ((v - 1.0446) / 0.0565537333333333)
        return t

    def hex_to_dec(self, s: str) -> int:
        """
        Convert a hexadecimal string to decimal.

        Args:
            s (str): The hexadecimal string.

        Returns:
            int: The decimal value.
        """
        return int(s, 16)

    def dec_to_hex(self, n: int, pad: int = 0) -> str:
        """
        Convert a decimal number to hexadecimal string.

        Args:
            n (int): The decimal number.
            pad (int): The number of digits to pad the result to.

        Returns:
            str: The hexadecimal string.
        """
        s = f"{n:X}"
        if pad == 0:
            return s
        else:
            return s.rjust(pad, "0")
