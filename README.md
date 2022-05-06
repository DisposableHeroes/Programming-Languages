# Programming-Languages Final Project

########## Documentation ##########

Akshat Chandra
Project: Try and Implement my own version of BASIC programming language in the style of Python.

Result: I wanted to implement something which allows for basic arithmetic operations and strings as input, but I was only able to succeed in implementing the former.

Running the Code: simply type "python3 shell.py" in the command line



Summary: After doing some research, I came to the conclusion that the followings three elements were essential to build my code:

 1) Tokenizer - This is needed to convert characters into "tokens." The tokens are then parsed and analyzed syntactically. I created a Tokenizer Class (and a Token class)
                which accepts text input for processing and scans it character by character. It then creates tokens which correspond to the type of input.

 2) Parser - The parser takes in a list of tokens and, like the Tokenizer, also tracks the index of the current token. It also checks if the token is an integer or a float
             and takes into account the order of operations. I learnt that the tree of nodes the parser tkaes in is called an "Abstract Syntax Tree."

 3)Interpreter - The interpreter takes in a node, processes it, and visits the child nodes. Since we have more than one node type (e.g. Binary, Unary), I
                 wrote a different visit method for each type. The interpreter then determines what method to call based on the type of node.


I don't think there's any code in particular which I would single out as being especially unique.
Every part of the project was pretty interesting to work on and had its own unique challenges. I definitely learnt a lot about writing languages.

Resources which helped me:
 https://www.freecodecamp.org/news/the-programming-language-pipeline-91d3f449c919/
 https://medium.com/swlh/writing-a-parser-getting-started-44ba70bb6cc9
 https://edu.anarcho-copy.org/Programming%20Languages/Go/writing%20an%20INTERPRETER%20in%20go.pdf


I also created a short video demo of my code.
