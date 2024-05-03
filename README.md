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
The system utilizes advanced natural language processing (NLP) techniques to generate concise summaries of uploaded documents and webpage urls.
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
1. Upon accessing the application, users are presented with options to register or login.
2. To register, users can click on the "Register" button and fill out the registration form with a unique username and password.
3. After registration, users can log in using their credentials.
4. Once logged in, users are redirected to the dashboard, where they can access various functionalities.
5. The dashboard allows users to upload documents, analyze uploaded documents, analyze web pages, or logout.
6. The application will return a summary, keywords, relevant URLs to online articles related to the content, and the tone of the text.

Workflow:
The application is built using Flask and consists of several routes:
1. /: The main route where users can register, login, or exit the application.
2. /register: Allows users to register for an account.
3. /login: Handles user authentication and redirects to the dashboard upon successful login.
4. /dashboard: Provides access to various functionalities like uploading documents and analyzing them or inputting an url and analyzing the text.
5. /upload_document: Allows users to upload documents.
6. /analyze_document: Summarizes and analyzes uploaded documents.
7. /analyze_webpage: Summarizes and analyzes web pages by providing a URL.
The app.py file defines the Flask application and contains all the route handlers for different functionalities.

Instructions for Developers
1. Clone the repository to your local environment.
2. Install the required dependencies specified in requirements.txt.
3. Ensure that MongoDB is installed and running locally or update the database configuration to point to the desired MongoDB instance.
4. Run the Flask application by executing the app.py file.
5. Run the uploader API and authenticate API inside /uploader and /authenticate respectively.
6. Access the application in your web browser at http://localhost:5002.
7. Develop additional features, enhance existing functionalities, or contribute to the project as needed.
8. Before committing any changes, ensure that all code follows the project's coding standards and conventions.
9. Create a pull request for review and integration of your changes into the main branch.
