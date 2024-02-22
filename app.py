from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import random
import os
from quotes import quotes  # Assuming quotes is a list of quotes

app = Flask(__name__)

@app.route('/generate_image', methods=['GET'])  # Change the method to GET
def generate_image():
    if not quotes:
        return "No quotes available", 500  # Return an error response if quotes list is empty
    quote, author = random.choice(quotes)
    author = f'- {author}'
    #quote = quotes[-1][0]

    # Load background image
    image_path = "./background.jpg"
    background_image = Image.open(image_path)

    # Create drawing context
    draw = ImageDraw.Draw(background_image)

    # Define font and size
    quote_font_path = "./Philosopher-Italic.ttf"
    author_font_path = "./Rambla-Italic.ttf"
    quote_font_size = 0
    if len(quote) < 100:
        quote_font_size = 30
        wrapped_quote = wrap(quote, width=25)  # Adjust the width as needed
    elif len(quote) < 160:
        quote_font_size = 25
        wrapped_quote = wrap(quote, width=25)  # Adjust the width as needed
    elif len(quote) < 200:
        quote_font_size = 20
        wrapped_quote = wrap(quote, width=30)  # Adjust the width as needed
    else:
        quote_font_size = 15
        wrapped_quote = wrap(quote, width=40)  # Adjust the width as needed
    quote_font = ImageFont.truetype(quote_font_path, size=quote_font_size)

    size=30
    if len(author) < 8:
        x_distance = 220
    elif len(author) < 12:
        x_distance = 190
    elif len(author) < 15:
        x_distance = 150
    elif len(author) < 19:
        x_distance = 100
    elif len(author) < 22:
        x_distance = 80
    else:
        x_distance = 80
        size=25
    
    author_font = ImageFont.truetype(author_font_path, size=size)
    # Calculate the height of the text box
    text_height = sum(draw.textbbox((0, 0), line, font=quote_font)[3] - draw.textbbox((0, 0), line, font=quote_font)[1] for line in wrapped_quote)

    # define and redefine the initial y position
    move_up_by = 50
    quote_y = ((background_image.height - text_height) // 2) - move_up_by

    # Set text color
    text_color = (255, 255, 255)  # White color
    draw.text((x_distance, 175), author, fill=text_color, font=author_font) # Draw the author's name on the image
    text_color = (171, 210, 0)  # Neone Green Color color


    for line in wrapped_quote:
        # Calculate x position for this line
        x = (background_image.width - draw.textbbox((0, 0), line, font=quote_font)[2]) // 2

        # Draw the text on the image
        draw.text((x, quote_y), line, fill=text_color, font=quote_font)

        # Update the y position for the next line
        quote_y += draw.textbbox((0, 0), line, font=quote_font)[3] - draw.textbbox((0, 0), line, font=quote_font)[1]

    

    # Save the modified image
    output_image_path = os.path.join(os.getcwd(), "output_image.jpg")
    background_image.save(output_image_path)

    # Send the image file to the client
    return send_file(output_image_path, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)  # For development purposes, switch to False in production
