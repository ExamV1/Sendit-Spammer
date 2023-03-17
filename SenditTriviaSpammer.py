import requests
import random
import time
import re
import html
import lxml.html
from lxml import html

#trivia api
url = "https://opentdb.com/api.php"
params = {
    "amount": 1, 
    "type": 'multiple',
}
print('.----------------.')
print('| Made By ExamV1 |')
print("'----------------'")
print('This will spam a bunch of random trivia questions to the chosen sendit')
sticker_link = input("\nEnter the sendit link: ")
match = re.search(r's/([a-f\d-]+)', sticker_link)
sticker_id = match.group(1)


while True:
    response = requests.get(url, params=params)
    data = response.json()
    questions = [lxml.html.fromstring(q["question"]).text_content() for q in data["results"]]
    answers = [lxml.html.fromstring(q["correct_answer"]).text_content() for q in data["results"]]
    incorrect_answers = [[lxml.html.fromstring(answer).text_content() for answer in q["incorrect_answers"]] for q in data["results"]]




    page1 = requests.get(sticker_link)
    soup1 = html.fromstring(page1.content)
    script_text1 = soup1.xpath('/html/body/script[1]/text()')[0]
    author_display_name = soup1.xpath('//*[@id="postedByText"]/span/text()[1]')[0]  #this gets the display name
    matches1 = re.findall(r'"(\w+)":\s*{"id":\s*"([^"]+)"', script_text1)  #this gets the unique id of the user you are sending to

    for i1, match1 in enumerate(matches1):
        if i1 == 1:                             #this makes sure it gets the correct user id and outputs it correctly
            var_id1 = match1[1]  

#the send post 
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

#makes sure the answer is in a random spot, aswell as the incorrect ones
    for i in range(len(questions)):
        choices = [answers[i]] + incorrect_answers[i]
        random.shuffle(choices)

        prompt = f"{questions[i]}\n\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n"
        data = {
            "data": {
                "postType": "sendit.post-type:question-and-answer-v1",
                "userId": var_id1,
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
        print("\nTrivia Qeuestion spam sent to sendit user: " + author_display_name + "\n#user id: " + var_id1)



        def loading_line(length):
            return ''.join(random.choice(['-', '=']) for _ in range(length))

        print(loading_line(10)) # this is just so you know if the code has not stopped
