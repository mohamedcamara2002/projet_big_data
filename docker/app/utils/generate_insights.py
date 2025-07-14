import boto3
import pandas as pd
import io

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    region_name='us-east-1',
)

response = s3.get_object(Bucket='inflation', Key='inflation_data.csv')
data = pd.read_csv(io.BytesIO(response['Body'].read()))

pays = ['Senegal', 'Mali', 'Mauritania', 'Gambia', 'Guinea']
selected_data = data[data['Country'].isin(pays)].copy()

def get_decade(year):
    if 2000 <= year <= 2009:
        return "2000-2009"
    elif 2010 <= year <= 2019:
        return "2010-2019"
    elif 2020 <= year <= 2022:
        return "2020-2022"
    else:
        return "Autre"

selected_data['Décennie'] = selected_data['Year'].apply(get_decade)

pivot = selected_data.pivot_table(
    values='Inflation',
    index='Country',
    columns='Décennie',
    aggfunc='mean'
).round(2)

rapport = "# Rapport d'Inflation – Afrique de l’Ouest (2000–2022)\n\n"
rapport += "Ce rapport présente les moyennes d'inflation par pays et par décennie.\n\n"
rapport += pivot.to_markdown()  # Génère le tableau Markdown

with open("rapport_inflation_2018_2022.md", "w") as f:
    f.write(rapport)

with open("rapport_inflation_2018_2022.md", "rb") as f:
    s3.put_object(
        Bucket="insights",
        Key="rapport_inflation_2018_2022.md",
        Body=f,
        ContentType="text/markdown"
    )

print("✅ Rapport généré et envoyé dans MinIO : insights/rapport_inflation_2018_2022.md")
