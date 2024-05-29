from flask import Flask, Response
import g4f

app = Flask(__name__)


def generate_initial_html(topic):
    prompt = f"Generate the body of what would be a page about {topic}."
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an internet webpage generator tasked with generating the body of an engaging HTML page with inline CSS about the following topic. Ensure the HTML includes a main header for the topic name and creatively present information related to the topic. Do not use images. Do not say anything except the html code."
            },
            {"role": "user", "content": prompt}
        ]
    )
    html_content = "<!DOCTYPE html><html><head><title>" + topic + "</title><style>body { font-family: Arial, sans-serif; }</style></head><body>" + \
                   response + "</body></html>"
    return html_content


def get_image_suggestions(topic):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a creative assistant. Suggest ideas for images that could complement an HTML page about the following topic. An idea is just a description of an image, nothing else. Please suggest at least 2 images. Separate each idea with a semicolon ;"
            },
            {"role": "user", "content": topic}
        ]
    )
    suggestions = response
    return suggestions.split(';')  # Assuming suggestions are semicolon-separated


# Placeholder for DALL·E image generation - this function is conceptual and needs actual implementation
def generate_images(image_descriptions):
    generated_images = []
    from g4f.client import Client

    client = Client()

    for description in image_descriptions:
        response = client.images.generate(
            model="dall-e",
            prompt=description,
        )
        image_url = response.data[0].url
        generated_images.append(image_url)
    return generated_images

def integrate_images(topic, urls, html_code):
    prompt = f"The topic is {topic}. The urls are {urls}. The base html page without any images is {html_code}"
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an internet webpage generator tasked with integrated images into existing html body. You will only output the updated html code and nothing else. the page is about a specific topic and you will be given image urls and their description so you can place them at the right locations."
            },
            {"role": "user", "content": prompt}
        ]
    )
    html_content = "<!DOCTYPE html><html><head><title>" + topic + "</title><style>body { font-family: Arial, sans-serif; }</style></head><body>" + \
                   response + "</body></html>"
    return html_content


@app.route('/p/<topic>')
def generate_page(topic):
    # Step 1: Generate initial HTML content
    html_content = generate_initial_html(topic)

    # # Step 2: Get image suggestions (This step is conceptual. Adjust according to actual implementation)
    # image_suggestions = get_image_suggestions(topic)
    #
    # # Step 3: Generate images based on suggestions (This requires actual DALL·E API integration)
    # images = generate_images(image_suggestions)
    #
    # # Step 4: Integrate images into HTML content (This is a basic example. Adjust as needed)
    # html_content = integrate_images(topic, images, html_content)
    # Step 5: Serve the updated HTML Page
    return Response(html_content, mimetype='text/html')


if __name__ == '__main__':
    app.run(debug=True)
