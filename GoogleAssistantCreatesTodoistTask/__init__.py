# -*- coding: utf-8 -*-
import logging
import azure.functions as func

import todoist
import re
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Todoist writer has been called.')

    text = req.params.get('text')

    apikey = os.environ['TODOIST_API_KEY']
    splitKeywords = os.environ['SPLIT_KEYWORDS']

    projectName = None
    if "TODOIST_PROJECT_NAME" in os.environ:
        projectName = os.environ['TODOIST_PROJECT_NAME']

    projectId = None
    if "TODOIST_PROJECT_ID" in os.environ:
        projectId = os.environ['TODOIST_PROJECT_ID']

    if text:
        #connect to api
        api = todoist.TodoistAPI(apikey)

        if not projectId and not projectName:
            raise AssertionError('both project_id and project_name aren''t set') 
        elif not projectId and projectName:
            logging.info(f'no project id given, loading via api call for {projectName}')
            api.sync()
            project = [p for p in api.state['projects'] if p['name'] == projectName][0]
            projectId = project['id']
        else:
            logging.info('Using project id from environment')

        logging.info(f'Using id {projectId}.')

        #split on keywords
        g = re.match(f'(.*)\b({splitKeywords})\b(.*)|(.*)', text).groups()

        #create todoist task
        try:
            item1 = api.items.add('%s%s' % (g[0] or '', g[3] or ''), projectId, date_string=g[2])
            api.commit()
        except SyncError:
            logging.warn('Looks like an invalid date string, so just use the full text')
            item1 = api.items.add(text, projectId)
            api.commit()

        return func.HttpResponse(f"Created Todoist task {text}!")
    else:
        return func.HttpResponse(
             "Please pass a text on the query string,
             status_code=400
        )
