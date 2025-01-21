// script.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("User guide loaded and ready!");

  // Automatically adjust sections to full viewport height
  const adjustSections = () => {
    const sections = document.querySelectorAll("section");
    sections.forEach((section) => {
      section.style.width = `${window.innerWidth}px`;
      section.style.height = `${window.innerHeight}px`;
    });
  };

  window.addEventListener("resize", adjustSections);
  adjustSections(); // Initial adjustment

  // Highlight section on scroll
  const sections = document.querySelectorAll("section");
  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    sections.forEach((section) => {
      if (
        section.offsetTop <= scrollPosition + 100 &&
        section.offsetTop + section.offsetHeight > scrollPosition
      ) {
        section.style.backgroundColor = "#e9f7ff";
      } else {
        section.style.backgroundColor = "white";
      }
    });
  });
});
