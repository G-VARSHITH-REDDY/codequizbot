import mysql.connector
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="root",  # Replace with your MySQL password
    database="codequizbot"
)

cursor = db.cursor()

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenization
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]  # Lemmatization and stop word removal
    return tokens

def get_question():
    cursor.execute("SELECT id, question FROM questions ORDER BY RAND() LIMIT 1;")
    return cursor.fetchone()

def get_answer(question_id):
    cursor.execute("SELECT answer FROM questions WHERE id = %s;", (question_id,))
    return cursor.fetchone()[0]

def process_question(user_input):
    user_tokens = preprocess_text(user_input)
    cursor.execute("SELECT id, question FROM questions;")
    questions = cursor.fetchall()
    for question_id, question_text in questions:
        question_tokens = preprocess_text(question_text)
        if all(token in question_tokens for token in user_tokens):
            return question_id
    return None

def chat():
    print("Welcome to CODEQUIZBOT! Type 'exit' to quit.")
    while True:
        user_input = input("Ask a question: ")
        if user_input.lower() == 'exit':
            break
        question_id = process_question(user_input)
        if question_id:
            answer = get_answer(question_id)
            print("Answer:", answer)
        else:
            print("Sorry, I don't know the answer to that question.")

if __name__ == "__main__":
    # Download necessary NLTK data
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    
    chat()
