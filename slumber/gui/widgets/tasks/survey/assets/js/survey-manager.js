function initializeSurvey(surveyJson) {
    Logger.info('Survey', 'Initialization started', { config: surveyJson.title });
    
    const survey = new Survey.Model(surveyJson);
    
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

    return survey;
}