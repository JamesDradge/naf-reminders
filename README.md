# naf-reminders
A web scraping project to send reminders of when a nail salon releases their calendar bookings

A couple of areas I want to come back to on this and improve

1. Use env variables for Twilio account settings and phone numbers, currently just have had to redact these
2. Better usage of stringified variables, so I don't have to wrap all my times in str() when I want to use them in logs
3. Better logging in general
4. Usage of if/or logic to account for BST, currently have this hardcoded and need to remember to change it


For deployment
Remember to remove the end call to reminderBot() and to add 'data, context' as arguments to the Cloud Platform function
