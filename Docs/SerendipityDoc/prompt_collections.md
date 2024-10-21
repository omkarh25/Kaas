1. Also don't forget to use SOLID principles in coding. 
2. Always add doc strings wherever applicable. 
3. Add good log statements while coding.

Analyze excel and create schema (chat gpt):
I need to build a web app using this companies financial excel data. Goal is to create a schema for each of the sheets from this Excel describing all the sheets and each of their header columns with data types and possible Enums where applicable. Ignore 'Dashboard' sheets from the schema. This schema will used make an LLM understand to create the web app. Provide the schema and sample data in .md format so its easier to use. Let's work on this iteratively. Take a look at all the sheets of the file first and give a brief description of each sheet. Next we can create a meaninful schema with sample data with datatypes, formats and enums for the each of the sheets analyzed.

Design Guideline:

Deployment 

General:
1. Design using SOLID principles. 
2. Add adequate logging for easier debugging. 
3. The app should have simple authentication using sqllite. with 2 levels of authorization: admin, view only.

Deployment Config:

Backend:
Techstack: Python 3.11, Pydantic, loguru, Pytest


Frontend:
1. It should support CRUD, sort and filter operations on all data tables, data visualization, and provide notifications for upcoming financial obligations. 
2. Use Shad-cn components for UI elements and ensure the app is mobile-responsive. 

Testing:




Past prompts:
I need next js to display, crud, sort and filter the given excel data screenshot