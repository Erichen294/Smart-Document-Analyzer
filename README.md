Smart Document Analyzer

Description:
The Smart Document Analyzer is a versatile tool designed to enhance document management and analysis processes. It provides functionalities for uploading, summarizing, and analyzing documents, empowering users to extract valuable insights from their textual content efficiently.

Features:

1. User Registration and Authentication:
Users can register for an account to access the system.
Secure authentication ensures that only authorized users can interact with the application.

2. Document Upload:
Users can upload various types of documents, including text files (e.g., .txt), PDFs, images, and more.
Uploaded documents are securely stored in the system for further analysis.

3. Document Summarization:
The system utilizes advanced natural language processing (NLP) techniques to generate concise summaries of uploaded documents.
Summaries provide users with a quick overview of the main points and key insights contained within the documents.

4. Keyword Extraction:
Keywords are automatically extracted from documents to highlight important terms and concepts.
Extracted keywords can aid in categorizing, searching, and organizing documents effectively.

5. Integration with External APIs:
The Smart Document Analyzer integrates with external APIs to enrich document analysis capabilities.
Integration with web search APIs allows users to retrieve relevant articles or resources related to document content.

6. User-Friendly Interface:
The application features an intuitive user interface for seamless interaction.
Clear navigation and straightforward functionalities make it easy for users to upload, analyze, and manage documents.

Usage:
Initially the user is greeted with 3 options, 1 to register, 2 to login and 3 to exit the application. If the user chooses to register, they can create their username and password which will be hashed and recorded in the MongoDB database. Each username must be unique or an error will be presented. Once the user is able to register, they can press 2 to login with their credentials. Once logged in, they can upload documents which will be stored under their account. Once the user has documents in the database, they can press 2 to analyze any documents that they have uploaded. The user will be presented with a summary, keywords, and online articles that they might be interested in reading. The user can logout by entering 3 and another subsequent 3 will exit the application.

Workflow:
The Github workflow dockers the entire application and runs both apis (authenticate and upload) then runs main.py. It will not do anything since the application expects user input. The dockerfile will dockerize the start_services.apy which starts both apis and then main.py.
