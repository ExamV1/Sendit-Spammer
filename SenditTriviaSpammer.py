import requests
import random
import time
import re
import html
import lxml.html
from lxml import html

# Set the API endpoint and parameters
url = "https://opentdb.com/api.php"
params = {
    "amount": 1, # number of questions to generate
    "type": 'multiple',
}
print('This will spam a bunch of random trivia questions to the chosen sendit')
sticker_link = input("\nEnter the sendit link: ")
match = re.search(r's/([a-f\d-]+)', sticker_link)
sticker_id = match.group(1)

while True:
    # Send a GET request to the API
    response = requests.get(url, params=params)

    # Extract the questions and answers from the response JSON
    data = response.json()
    questions = [lxml.html.fromstring(q["question"]).text_content() for q in data["results"]]
    answers = [lxml.html.fromstring(q["correct_answer"]).text_content() for q in data["results"]]
    incorrect_answers = [[lxml.html.fromstring(answer).text_content() for answer in q["incorrect_answers"]] for q in data["results"]]

    # Extract the author name from the sticker link using XPath
    page = requests.get(sticker_link)
    soup = html.fromstring(page.content)
    author_display_name = soup.xpath('//*[@id="postedByText"]/span/text()[1]')[0]

    #Send the questions and answers
    send_url = "https://reply.getsendit.com/api/v1/sendpost"
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "content-type": "text/plain;charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    for i in range(len(questions)):
        choices = [answers[i]] + incorrect_answers[i]
        random.shuffle(choices)

        # Construct the question message that gets sent, including the author name
        prompt = f"{questions[i]}\n\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n"
        data = {
            "data": {
                "postType": "sendit.post-type:question-and-answer-v1",
                "userId": "f339d5f5-2c0e-4634-99ad-dae3adeb0dcf",
                "stickerId": sticker_id,
                "shadowToken": "ffe4b23a-5977-435a-8109-d57cfb4ab6e2",
                "platform": "snapchat",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69"
            },
            "replyData": {
                "question": prompt,
                "promptText": ""
            }
        }

        response = requests.post(send_url, headers=headers, json=data)

        #more debug PRINT info
        #print("Response Status Code:", response.status_code)
        #print("Response Text:", response.text)
        print("Trivia Qeuestion spam sent to sendit user: " + author_display_name)

        # Wait in seconds before sending the next question, add a wait if you expeience program crashing
        time.sleep(0.01)
        #but if you want to try make it spam faster remove the time.sleep
