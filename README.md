# greet-cli prototype

## About

> ❔ The following is a description concerning the context of the problem addressed with this fork. You can find the original abstract for ProjectSunshine on the main repository (https://github.com/SCANL/ProjectSunshine)

Linguistic antipatterns are problems related to the naming of elements in the source code of a software project. They cause inconsistencies, ambiguity, and confusion in the code, making it less easy to understand, hence it may be difficult for developers to maintain it. For this reason, they are considered a bad code practice. In the context of AI systems, these antipatterns are even more crucial due to their built-in complexity. Unfortunately, there is currently no tool available that can detect these antipatterns in Python code and notify developers about them. Furthermore, Python is a critical language for AI-based systems, being the most used language for this kind of software [1].

The only tool supporting this analysis is IDEAL, which supports only C# and Java. It's written in Python and it is also packaged as an IntelliJ IDEA plugin.

This tool analyzes the code to search for antipatterns defined by Arnaoudova et al. [2], which are divided into the following categories:

Ambiguity antipatterns: These antipatterns occur when the names of code elements are ambiguous, making it difficult to understand their meaning and purpose.
Synonym antipatterns: These antipatterns occur when synonyms are used for the same concept in different parts of the code, creating inconsistency and difficulty in understanding.
Homonym antipatterns: These antipatterns occur when different names are used to describe different elements in the code, creating confusion and errors.
False friend antipatterns: These antipatterns occur when code element names seem to correspond to a familiar concept, but in reality represent something different.
Verbose antipatterns: These antipatterns occur when code element names are too long and verbose, making it difficult to understand the code.

## Goals

The aim is to offer developers a tool that assists them in avoiding introducing linguistic antipatterns in Python source code, based on AI techniques instead of parsing and POS tagging techniques like the current tool, in order to experiment with a different approach to solving the problem and evaluate its results compared to the current solution and thereby preventing all the issues described in the preceding paragraph.

The current repository contains a prototype of the modification that will be integrated into IDEAL, enabling it to analyze and detect antipatterns in Python files as well. Currently, IDEAL supports only C# and Java languages, but with this ongoing modification, support for Python files, which are widely used in the context of AI-based systems, will be extended. This update will provide developers with the capability to identify and address linguistic antipatterns in their Python code, enhancing code quality and maintainability.

## Requirements

## Installation

## Functional Requirements

1. Supported languages: Python
2. Analyze one or more source code files:

- accept path to a directory or a file

3. The tool analyzes the following entities in a file:

- classes
- class variables
- methods
- method variables

4. Detected violations stored (optionally) in a file in JSON format.
5. Checks:

- get more than accessor
- not implemented condition
- method signature and comment are opposite
- attribute name and comment are opposite
