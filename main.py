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
      {"role": "system", "content": "You're an experienced writer who specializes in crafting personalized cover letters and resumes that are tailored to specific job listings. Your goal is to highlight the candidate's relevant experience, skills, and achievements that directly align with the job requirements. Ensure the cover letter effectively communicates the candidate's suitability for the position and their enthusiasm for the role."},
      {"role": "user", "content": resume},
      {"role": "user", "content": listing}
    ]
)

print(completion.choices[0].message)

