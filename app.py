from flask import Flask, render_template, request
import pickle
import numpy as np

dataset_df = pickle.load(open('dataset.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

# Define routes and functions

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(dataset_df['Book-Title'].values),
                           author=list(dataset_df['Book-Author'].values),
                           image=list(dataset_df['Image-URL-L'].values),
                           votes=list(dataset_df['num_ratings'].values),
                           rating=list(dataset_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
    pass

@app.route('/recommend_books', methods=['post'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
            data.append(item)

        return render_template('recommend.html', data=data, text=user_input)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return render_template('404.html'), 404

# Custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
