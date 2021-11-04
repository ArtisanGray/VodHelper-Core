# VodHelper 0.1.1

## Intro
VodHelper is a program that uses the Twitch API to create formatted files containing timestamps. Useful for editors and content creators alike.

VodHelper was created by Eli Greene.

### Here are some links that are relevant to the project:

[LinkedIn Profile](https://www.linkedin.com/in/artisangray/)

[Project Blog](https://www.linkedin.com/pulse/vodhelper-save-yourself-some-time-ethan-eli-greene)


## Installation

Not a lot of setup is needed for VodHelper - simply download the main.py file associated with the project and execute it - whether it be in an online interpreter, IDLE, a VM, etc.

## Usage

To use VodHelper, the only thing you need is a VOD ID from Twitch, which is as follows:

  ![Snippet of ID](https://github.com/ArtisanGray/VodHelper-Core/blob/main/id_snippet.png)

**The ID needed is the 10-20 digit number on the tail end of the Twitch URL**. Copy and paste into the prompt and the magic starts.

Once you've pressed <Enter>, An API request will be made using the ID given. If the Request is successful, it will return a "Found!" message and generate the timestamps. Otherwise, the program will close with an error. When the clip data has been gathered and the timestamp data has been generated and primed - a prompt will follow asking a question:

  ![Question Snippet](https://github.com/ArtisanGray/VodHelper-Core/blob/main/q_snippet.png)

*This was added from the perspective that editors, when given clips like these, often pick at random. A video baselessly showing off clips sorted from best to worst would be disingenuous and kind of...boring.*

**Output should look like this in the final file:** (the titles being placeholders and completely made up, in case that wasn't apparent.)
  
  ![Snippet of APP](https://github.com/ArtisanGray/VodHelper-Core/blob/main/ts_snippet.png)
  
