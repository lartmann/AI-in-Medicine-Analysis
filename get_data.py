import requests
import pandas as pd
import time

url = f"https://api.openalex.org/works?filter=from_publication_date:2019-01-01&per_page=200&cursor=*"
response = requests.get(url)
df = pd.DataFrame(response.json()['results'])
num_pages = int(response.json()['meta']['count']/200) + 1

print(f"Total pages: {num_pages}")
failed = []

def transform_data(response):
    titles = []
    ids = []
    dois = []
    publication_dates = []
    languages = []
    open_access = []
    host_organization_ids = []
    host_organization_names = []
    types = []
    authors_name = []
    authors_orcid = []
    authors_id = []
    author_positions = []
    institution_names = []
    institudion_countries = []
    institution_types = []
    institution_ids = []
    countries = []
    citations = []
    citation_normalized_percentiles = []
    domains = []
    fields = []
    subfields = []
    topics = []
    keywords = []
    concepts = []
    referenced_work_count = []
    abstract_words = []
    cited_by_api_urls = []
    counts_by_years = []
    abstract_words = []
    references = []

    results = response.json()['results']

    for i in range(len(results)):
        ids.append(results[i]['id'])
        titles.append(results[i]['title'])
        dois.append(results[i]['doi'])
        publication_dates.append(results[i]['publication_date'])
        languages.append(results[i]['language'])
        types.append(results[i]['type'])
        open_access.append(results[i]['open_access']['is_oa'])
        
        authors_name.append([author['author']['display_name'] for author in results[i]['authorships']])
        authors_orcid.append([author['author']['orcid'] for author in results[i]['authorships']])
        authors_id.append([author['author']['id'] for author in results[i]['authorships']])
        author_positions.append([author['author_position'] for author in results[i]['authorships']])
        # append institutions of the authors   
        institution_names.append([inst['display_name'] for author in results[i]['authorships'] for inst in author['institutions']])
        institution_ids.append([inst['id'] for author in results[i]['authorships'] for inst in author['institutions']])
        institution_types.append([inst['type'] for author in results[i]['authorships'] for inst in author['institutions']])
        institudion_countries.append([inst['country_code'] for author in results[i]['authorships'] for inst in author['institutions']])
        countries.append([author['countries'] for author in results[i]['authorships']])
        citations.append(results[i]['cited_by_count'])
        topics.append([t['display_name'] for t in results[i]['topics']])
        domains.append([t['domain']['display_name'] for t in results[i]['topics']])
        fields.append([t['field']['display_name'] for t in results[i]['topics']])
        subfields.append([t['subfield']['display_name'] for t in results[i]['topics']])
        keywords.append([t['display_name'] for t in results[i]['keywords']])
        concepts.append([t['display_name'] for t in results[i]['concepts']])
        referenced_work_count.append(results[i]['referenced_works_count'])
        cited_by_api_urls.append(results[i]['cited_by_api_url'])
        references.append(results[i]['referenced_works'])
        #abstract_words.append(dict(results[i]['abstract_inverted_index']).keys())
        counts_by_years.append(results[i]['counts_by_year'])

    res = {
        'title': titles,
        'id': ids,
        'doi': dois,
        'publication_date': publication_dates,
        'language': languages,
        'type': types,
        'open_access': open_access,
        'authors_name': authors_name,
        'authors_orcid': authors_orcid,
        'authors_id': authors_id,
        'authors_positions': author_positions,
        'institution_names': institution_names,
        'institution_ids': institution_ids,
        'institution_types': institution_types,
        'institudion_countries': institudion_countries,
        'countries': countries,
        'citations': citations,
        'topics': topics,
        'domains': domains,
        'fields': fields,
        'subfields': subfields,
        'keywords': keywords,
        'concepts': concepts,
        'referenced_work_count': referenced_work_count,
        'counts_by_years': counts_by_years,
        'references': references
    }
    return pd.DataFrame(res)
    
transform_data(response).to_csv('openalex_1.csv', index=False)

for i in range(2, num_pages):
    try: 
        url = f"https://api.openalex.org/works?filter=from_publication_date:2019-01-01&per_page=200&cursor={response.json()['meta']['next_cursor']}"
        response = requests.get(url)
        
        df = transform_data(response)
        # /mnt/mydrive/dataviz_data/
        df.to_csv(f'openalex_{i}.csv', index=False)
        if i % 10 == 0:
            print(f"Articles Retrieved: {i * 200}")
            #time.sleep(1)
    except:
        failed.append(i)
        print(f"Failed page: {i}")