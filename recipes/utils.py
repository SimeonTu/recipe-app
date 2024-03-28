from io import BytesIO
import base64
import matplotlib.pyplot as plt


def get_graph():
    # create a BytesIO buffer for the image
    buffer = BytesIO()

    # create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format='png')

    # set cursor to the beginning of the stream
    buffer.seek(0)

    # retrieve the content of the file
    image_png = buffer.getvalue()

    # encode the bytes-like object
    graph = base64.b64encode(image_png)

    # decode to get the string as output
    graph = graph.decode('utf-8')

    # free up the memory of buffer
    buffer.close()

    # return the image/graph
    return graph

# chart_type: user input o type of chart,
# data: pandas dataframe


def get_chart1(data, **kwargs):
    # switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    # AGG is preferred solution to write PNG files
    plt.switch_backend('AGG')

    fig, ax = plt.subplots(figsize=(10, 6))

    # Count the number of recipes by difficulty
    data['difficulty'].value_counts().plot(
        kind='bar', color=['skyblue', 'orange', 'green', 'red'], ax=ax)
    plt.title('Number of Recipes by Difficulty')
    plt.xlabel('Difficulty')
    plt.ylabel('Number of Recipes')
    # elif chart_type == 'pie':
    #     # For a pie chart example
    #     data['difficulty'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    #     plt.title('Recipes Distribution by Difficulty')
    # else:
    #     print("Unsupported chart type")

    plt.tight_layout()
    chart = get_graph()
    return chart


def get_chart2(data, **kwargs):
    plt.switch_backend('AGG')

    plt.figure(figsize=(10, 6))
    
    # Assuming 'data' is a DataFrame with 'difficulty' and 'average_cooking_time' columns
    plt.bar(data['difficulty'], data['average_cooking_time'],
            color=['skyblue', 'orange', 'green', 'red'])
    plt.title('Average Cooking Time by Difficulty')
    plt.xlabel('Difficulty')
    plt.ylabel('Average Cooking Time (minutes)')
    plt.xticks(rotation=45)  # Rotate difficulty labels for better readability
    plt.tight_layout()
    chart = get_graph()
    return chart
