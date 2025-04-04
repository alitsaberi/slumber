function initializeSurvey(surveyJson) {
    Logger.info('Survey', 'Initialization started', { config: surveyJson.title });
    
    const survey = new Survey.Model(surveyJson);
    survey.applyTheme(SurveyTheme.SharpDark);
    
    survey.pages.forEach((page, pageIndex) => {
        Logger.info('Survey', `Processing page ${pageIndex + 1}/${survey.pages.length}`, {
            pageTitle: page.title,
            elementCount: page.elements.length
        });
        
        page.elements.forEach((element, elementIndex) => {
            Logger.info('Survey', 'Element processed', {
                pageIndex,
                elementIndex,
                type: element.getType(),
                name: element.name,
                isRegistered: Survey.ElementFactory.Instance.getAllTypes().includes(element.getType())
            });
        });
    });

    survey.onComplete.add((sender) => {
        Logger.info('Survey', 'Survey completed', { 
            questionCount: Object.keys(sender.data).length 
        });
        window.channelObject?.handle_survey_submission(JSON.stringify(sender.data));
    });

    const converter = markdownit({
        html: true // Support HTML tags in the source (unsafe, see documentation)
    });
    survey.onTextMarkdown.add((_, options) => {
        // Convert Markdown to HTML
        let str = converter.renderInline(options.text);
        options.html = str;
    });

    return survey;
}