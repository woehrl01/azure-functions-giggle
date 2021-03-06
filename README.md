# azure-functions-giggle

Azure Function which can be used as Webhooks from [IFTTT](https://ifttt.com) and [Zapier](https://zapier.com) for better integration

Must be deployed with your own Azure subscription.

Currently Python is used for the functions. Please beware that **currently Python is in preview**.

Following settings must be configured via the Azure Portal:

## GoogleAssistantCreatesTodoistTask:

Webhook which can be used to create [Todoist](https://todoist.com) tasks, which tries to detect and fill in the due date.

### Required:

`TODOIST_API_KEY` with your API key for Todoist

`SPLIT_KEYWORDS` a Python Regex for keywords to split the provided text. e.g. `für|am|at|on`

### Either:

`TODOIST_PROJECT_NAME` the project name where the task should be created

`TODOIST_PROJECT_ID` the project id where the task should be created (can be useful if you rename your project or have emoijs in it)

`MIT License`