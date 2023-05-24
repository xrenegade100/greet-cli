# greet-cli prototype

## Functional Requirements

1. Supported languages: Python
2. Analyze one or more source code files:

-   accept path to a directory or a file

3. The tool analyzes the following entities in a file:

-   classes
-   class variables
-   methods
-   method variables

4. Detected violations stored (optionally) in a file in JSON format.
5. Checks:

-   get more than accessor
-   not implemented condition
-   method signature and comment are opposite
-   attribute name and comment are opposite
