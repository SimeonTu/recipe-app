from io import BytesIO
import base64
import matplotlib.pyplot as plt


def get_graph():
    # create a BytesIO buffer for the image
    buffer = BytesIO()

    # create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format='png')

    plt.close('all')  # This ensures the current figure is closed after saving

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


def categorize_cooking_times(recipes):
    # Define your ranges
    ranges = {
        '1-10 mins': 0,
        '11-20 mins': 0,
        '21-30 mins': 0,
        '31-40 mins': 0,
        '41-50 mins': 0,
        '51-60 mins': 0,
        '61+ mins': 0
    }

    # Categorize each recipe
    for time in recipes:
        if time <= 10:
            ranges['1-10 mins'] += 1
        elif time <= 20:
            ranges['11-20 mins'] += 1
        elif time <= 30:
            ranges['21-30 mins'] += 1
        elif time <= 40:
            ranges['31-40 mins'] += 1
        elif time <= 50:
            ranges['41-50 mins'] += 1
        elif time <= 60:
            ranges['51-60 mins'] += 1
        else:
            ranges['61+ mins'] += 1

    return ranges

# chart_type: user input o type of chart,
# data: pandas dataframe


def bar_chart_recipe_number_by_difficulty(data):
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


def pie_chart_recipes_by_cooking_time(df):
    plt.switch_backend('AGG')

    # Filter out 0% categories
    df_filtered = df[df['Number of Recipes'] > 0]

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        df_filtered['Number of Recipes'], autopct='%1.1f%%', startangle=140)

    # Improve readability
    plt.setp(autotexts, size=8, weight="bold")

    # Use a legend for labels to avoid clutter
    ax.legend(wedges, df_filtered['Cooking Time Range'],
              title="Cooking Time Ranges",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    ax.set_title('Recipe Distribution by Cooking Time Range')

    plt.tight_layout()

    chart = get_graph()
    return chart


def line_chart_ingredient_usage(data):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10, 6))
    # Sort data for better visualization, if not already sorted
    data = data.sort_values('total', ascending=True)
    plt.plot(data['name'], data['total'], marker='o',
             linestyle='-', color='skyblue')
    plt.title('Number of Recipes per Ingredient')
    plt.xlabel('Ingredient')
    plt.ylabel('Number of Recipes')
    plt.xticks(rotation=90)  # Rotate ingredient names for better readability
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    chart = get_graph()
    return chart