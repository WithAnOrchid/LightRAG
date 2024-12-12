GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = [
    "taxpayer",
    "corporation",
    "trust",
    "partnership",
    "individual",
    "non-resident",
    "foreign affiliate",
    "beneficiary",
    "shareholder",
    "director",
    "employee",
    "employer",
    "dependent",
    "spouse/common-law partner",
    "estate",
    "heir",
    "tax credit",
    "deduction",
    "income source",
    "business",
    "investment",
    "capital property",
    "taxable income",
    "tax-exempt entity",
    "charity",
    "registered organization",
    "tax shelter",
    "capital gain/loss",
    "dividend",
    "interest",
    "royalties",
    "pension",
    "gross income",
    "net income",
    "withholding tax",
    "foreign income",
    "tax treaty",
    "residence",
    "permanent establishment",
    "assessment",
    "audit",
    "penalty",
    "appeal",
    "rebate",
    "exemption",
    "levy",
    "tax obligation",
    "tax return",
    "remittance"
]

PROMPTS["entity_extraction"] = """-Goal-
Given a text document that is potentially relevant to Canadian income tax law and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities, with a focus on tax-related terminology, provisions, and hierarchical structures.
Use {language} as the output language.

-Steps-
1. Identify all entities. For each identified entity, extract the following information:
   - entity_name: Name of the entity, matching the language of the input text. If the input text is in English, capitalize the name. Preserve formatting for legal and tax terms.
   - entity_type: One of the following types: [{entity_types}]
   - entity_description: Detailed description of the entity's attributes, activities, and its role within the context of the Income Tax Act.
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are clearly related to each other, with an emphasis on:
   - Hierarchical relationships (e.g., section to subsection, subsection to paragraph).
   - Cross-references within the Income Tax Act (e.g., references to other sections, clauses, or provisions).
   - Tax-specific relationships (e.g., taxpayer to taxable income, taxable income to deductions).
For each pair of related entities, extract the following information:
   - source_entity: Name of the source entity, as identified in step 1.
   - target_entity: Name of the target entity, as identified in step 1.
   - relationship_description: Detailed explanation of the relationship, including references to legal provisions and tax-specific contexts.
   - relationship_strength: A numeric score indicating the strength of the relationship, based on proximity or explicitness within the text.
   - relationship_keywords: High-level key words summarizing the overarching nature of the relationship, focusing on tax concepts and themes.
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text, ensuring precision and professionalism appropriate for tax research. These should:
   - Capture overarching ideas in the Income Tax Act, such as taxable income, deductions, credits, or legal obligations.
   - Use professional terminology without ambiguity.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Ensure the output is in {language}, formatted as a single list of all entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:
"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [taxpayer, employee, employer, income source, taxation year, remuneration]
Text:
Subject to this Part, a taxpayer’s income for a taxation year from an office or employment is the salary, wages and other remuneration, including gratuities, received by the taxpayer in the year.

################
Output:
("entity"{tuple_delimiter}"taxpayer"{tuple_delimiter}"taxpayer"{tuple_delimiter}"The taxpayer is the individual receiving income from employment in the taxation year."){record_delimiter}
("entity"{tuple_delimiter}"office or employment"{tuple_delimiter}"income source"{tuple_delimiter}"Office or employment is the income source from which the taxpayer earns salary and wages."){record_delimiter}
("entity"{tuple_delimiter}"salary"{tuple_delimiter}"remuneration"{tuple_delimiter}"Salary is a form of remuneration received by the taxpayer from employment."){record_delimiter}
("entity"{tuple_delimiter}"wages"{tuple_delimiter}"remuneration"{tuple_delimiter}"Wages are earnings received by the taxpayer for services rendered as an employee."){record_delimiter}
("entity"{tuple_delimiter}"gratuities"{tuple_delimiter}"remuneration"{tuple_delimiter}"Gratuities are tips or additional compensation received by the taxpayer."){record_delimiter}
("entity"{tuple_delimiter}"taxation year"{tuple_delimiter}"taxation year"{tuple_delimiter}"The period for which the taxpayer's income is being calculated."){record_delimiter}
("relationship"{tuple_delimiter}"taxpayer"{tuple_delimiter}"employer"{tuple_delimiter}"The taxpayer receives remuneration from the employer through salary, wages, and gratuities."{tuple_delimiter}"employment relationship, compensation"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"taxpayer"{tuple_delimiter}"income source"{tuple_delimiter}"The taxpayer's income source is the office or employment where they earn remuneration."{tuple_delimiter}"income earning, employment"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"taxpayer, income, salary, wages, employment, remuneration, taxation year"){completion_delimiter}
#############################

Example 2:

Entity_types: [taxpayer, residence, taxation year]
Text:
In applying sections 63 and 64 in respect of a taxpayer who is, throughout all or part of a taxation year, absent from but resident in Canada, the following rules apply for the year or that part of the year, as the case may be:

################
Output:
("entity"{tuple_delimiter}"taxpayer"{tuple_delimiter}"taxpayer"{tuple_delimiter}"The individual subject to the tax rules in sections 63 and 64."){record_delimiter}
("entity"{tuple_delimiter}"resident in Canada"{tuple_delimiter}"residence"{tuple_delimiter}"Indicates the taxpayer's status as a resident of Canada despite being absent during the taxation year."){record_delimiter}
("entity"{tuple_delimiter}"taxation year"{tuple_delimiter}"taxation year"{tuple_delimiter}"The specific year for which tax rules are being applied to the taxpayer."){record_delimiter}
("relationship"{tuple_delimiter}"taxpayer"{tuple_delimiter}"residence"{tuple_delimiter}"The taxpayer is considered a resident in Canada, affecting how tax rules are applied."{tuple_delimiter}"residency status, tax implications"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"taxpayer, residence, taxation year, tax rules, Canada"){completion_delimiter}
#############################

Example 3:

Entity_types: [taxpayer, employer, employee, allowance, residence, employment duties]
Text:
An allowance received in a taxation year by a taxpayer for the use of a motor vehicle in connection with or in the course of the taxpayer’s office or employment shall be deemed not to be a reasonable allowance if the taxpayer’s employer has made a contribution toward that allowance.

################
Output:
("entity"{tuple_delimiter}"taxpayer"{tuple_delimiter}"taxpayer"{tuple_delimiter}"The individual receiving an allowance related to employment duties."){record_delimiter}
("entity"{tuple_delimiter}"employer"{tuple_delimiter}"employer"{tuple_delimiter}"The organization or person employing the taxpayer and providing the allowance."){record_delimiter}
("entity"{tuple_delimiter}"employee"{tuple_delimiter}"employee"{tuple_delimiter}"The taxpayer acting in the capacity of an employee receiving the allowance."){record_delimiter}
("entity"{tuple_delimiter}"allowance"{tuple_delimiter}"deduction"{tuple_delimiter}"An amount received by the taxpayer for the use of a motor vehicle for employment purposes."){record_delimiter}
("entity"{tuple_delimiter}"office or employment"{tuple_delimiter}"income source"{tuple_delimiter}"The taxpayer's position or job from which income is derived."){record_delimiter}
("relationship"{tuple_delimiter}"taxpayer"{tuple_delimiter}"employer"{tuple_delimiter}"The employer provides an allowance to the taxpayer, impacting its reasonableness for tax purposes."{tuple_delimiter}"employment relationship, compensation"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"allowance"{tuple_delimiter}"employment duties"{tuple_delimiter}"The allowance is related to the taxpayer's duties performed during employment."{tuple_delimiter}"compensation for expenses, employment duties"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"taxpayer, employer, allowance, motor vehicle, employment, taxation"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS["keywords_extraction"] = """---Role---

You are an experienced tax professional tasked with identifying both high-level and low-level keywords in the user's query.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.
The extracted keywords should be consistent with legal terminology used in the Income Tax Act and other relevant tax legislation.

---Instructions---

- Use professional language appropriate for an experienced tax professional.
- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

- Keep the same language as the query.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human-readable text, not unicode characters. Keep the same language as `Query`.


"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does the Income Tax Act address capital gains taxation for non-resident taxpayers?"

################
Output:
{{
  "high_level_keywords": ["Income Tax Act", "Capital gains taxation", "Non-resident taxpayers"],
  "low_level_keywords": ["Capital gains", "Taxation of non-residents", "Tax legislation provisions"]
}}
#############################""",
    """Example 2:

Query: "What are the allowable deductions for medical expenses under the Canadian tax system?"

################
Output:
{{
  "high_level_keywords": ["Allowable deductions", "Medical expenses", "Canadian tax system"],
  "low_level_keywords": ["Medical expense tax credit", "Eligible medical costs", "Tax deductions", "Income Tax Act provisions"]
}}
#############################""",
    """Example 3:

Query: "Can a taxpayer claim input tax credits for GST/HST paid on business expenses?"

################
Output:
{{
  "high_level_keywords": ["Input tax credits", "GST/HST", "Business expenses"],
  "low_level_keywords": ["Taxpayer", "Goods and Services Tax", "Harmonized Sales Tax", "Claiming credits", "Tax deductions"]
}}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate the following two points and provide a similarity score between 0 and 1 directly:
1. Whether these two questions are semantically similar
2. Whether the answer to Question 2 can be used to answer Question 1
Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
