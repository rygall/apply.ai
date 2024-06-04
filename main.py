from openai import OpenAI
client = OpenAI()


listing = None
with open('listing.txt', 'r') as file:
    listing = file.read().replace('\n', '')

resume = None
with open('resume.txt', 'r') as file:
    resume = file.read().replace('\n', '')


completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
      {"role": "system", "content": "You are a professional writer that writes resumes and cover letters for people that is specific to a job listing they want to apply to."},
      {"role": "user", "content": resume},
      {"role": "user", "content": listing}
    ]
)

print(completion.choices[0].message)

