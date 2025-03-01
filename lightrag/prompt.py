from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "Vietnamese"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = entities = ["Book", "Author", "Publisher", "Manufacturer", "Seller", "Genre", "Series", "Price", "Sold Quantity", "Discount", "Rating"]

PROMPTS["entity_extraction"] = """---Goal---
Given a text document that contains information about books, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

---Steps---
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Tên của thực thể (ví dụ: tên sách, tên tác giả, nhà xuất bản, nhà bán, thể loại). Giữ nguyên ngôn ngữ của văn bản đầu vào.
- entity_type: One of the following types: [{entity_types}]
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other (e.g. "written by", "published by", "sold by", "of genre")
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity (eg 10 for direct relations like "written by", lower for indirect relations)
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [Book, Author, Publisher, Seller, Price, Rating]
Text:
Sách "Bản Đồ" được viết bởi Aleksandra Mizielińska, Daniel Mizieliński.
Sách "Bản Đồ" có giá 224250 VND.
Sách "Bản Đồ" được xuất bản bởi Nhã Nam.
Sách "Bản Đồ" có đánh giá trung bình 4.8 sao.
Sách "Bản Đồ" cũng được bán bởi nha sach nguyet linh với giá 325000 VND.
################
Output:
("entity"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"Book"{tuple_delimiter}"Cuốn sách có tên 'Bản Đồ'")##
("entity"{tuple_delimiter}"Aleksandra Mizielińska"{tuple_delimiter}"Author"{tuple_delimiter}"Tác giả của sách 'Bản Đồ'")##
("entity"{tuple_delimiter}"Daniel Mizieliński"{tuple_delimiter}"Author"{tuple_delimiter}"Tác giả của sách 'Bản Đồ'")##
("entity"{tuple_delimiter}"Nhã Nam"{tuple_delimiter}"Publisher"{tuple_delimiter}"Nhà xuất bản của sách 'Bản Đồ'")##
("entity"{tuple_delimiter}"224250 VND"{tuple_delimiter}"Price"{tuple_delimiter}"Giá chính của sách 'Bản Đồ'")##
("entity"{tuple_delimiter}"4.8 sao"{tuple_delimiter}"Rating"{tuple_delimiter}"Đánh giá trung bình của sách 'Bản Đồ'")##
("entity"{tuple_delimiter}"nha sach nguyet linh"{tuple_delimiter}"Seller"{tuple_delimiter}"Nhà bán sách 'Bản Đồ'")##
("entity"{tuple_delimiter}"325000 VND"{tuple_delimiter}"Price"{tuple_delimiter}"Giá của sách 'Bản Đồ' tại nha sach nguyet linh")##
("relationship"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"Aleksandra Mizielińska"{tuple_delimiter}"Sách 'Bản Đồ' được viết bởi Aleksandra Mizielińska"{tuple_delimiter}"tác giả"{tuple_delimiter}10)##
("relationship"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"Daniel Mizieliński"{tuple_delimiter}"Sách 'Bản Đồ' được viết bởi Daniel Mizieliński"{tuple_delimiter}"tác giả"{tuple_delimiter}10)##
("relationship"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"Nhã Nam"{tuple_delimiter}"Sách 'Bản Đồ' được xuất bản bởi Nhã Nam"{tuple_delimiter}"xuất bản"{tuple_delimiter}10)##
("relationship"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"224250 VND"{tuple_delimiter}"Sách 'Bản Đồ' có giá chính 224250 VND"{tuple_delimiter}"giá cả"{tuple_delimiter}10)##
("relationship"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"4.8 sao"{tuple_delimiter}"Sách 'Bản Đồ' có đánh giá trung bình 4.8 sao"{tuple_delimiter}"đánh giá"{tuple_delimiter}10)##
("relationship"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"nha sach nguyet linh"{tuple_delimiter}"Sách 'Bản Đồ' được bán bởi nha sach nguyet linh"{tuple_delimiter}"bán hàng"{tuple_delimiter}8)##
("relationship"{tuple_delimiter}"Bản Đồ"{tuple_delimiter}"325000 VND"{tuple_delimiter}"Sách 'Bản Đồ' có giá 325000 VND tại nha sach nguyet linh"{tuple_delimiter}"giá cả"{tuple_delimiter}8)##
("relationship"{tuple_delimiter}"325000 VND"{tuple_delimiter}"nha sach nguyet linh"{tuple_delimiter}"Giá 325000 VND được cung cấp bởi nha sach nguyet linh"{tuple_delimiter}"bán hàng"{tuple_delimiter}10)##
("content_keywords"{tuple_delimiter}"bán sách, giá sách, đánh giá sách")<|COMPLETE|>
#############################""",
    """Example 2:

Entity_types: [person, technology, mission, organization, location]
Text:
They were no longer mere operatives; they had become guardians of a threshold, keepers of a message from a realm beyond stars and stripes. This elevation in their mission could not be shackled by regulations and established protocols—it demanded a new perspective, a new resolve.

Tension threaded through the dialogue of beeps and static as communications with Washington buzzed in the background. The team stood, a portentous air enveloping them. It was clear that the decisions they made in the ensuing hours could redefine humanity's place in the cosmos or condemn them to ignorance and potential peril.

Their connection to the stars solidified, the group moved to address the crystallizing warning, shifting from passive recipients to active participants. Mercer's latter instincts gained precedence— the team's mandate had evolved, no longer solely to observe and report but to interact and prepare. A metamorphosis had begun, and Operation: Dulce hummed with the newfound frequency of their daring, a tone set not by the earthly
#############
Output:
("entity"{tuple_delimiter}"Washington"{tuple_delimiter}"location"{tuple_delimiter}"Washington is a location where communications are being received, indicating its importance in the decision-making process."){record_delimiter}
("entity"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"mission"{tuple_delimiter}"Operation: Dulce is described as a mission that has evolved to interact and prepare, indicating a significant shift in objectives and activities."){record_delimiter}
("entity"{tuple_delimiter}"The team"{tuple_delimiter}"organization"{tuple_delimiter}"The team is portrayed as a group of individuals who have transitioned from passive observers to active participants in a mission, showing a dynamic change in their role."){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Washington"{tuple_delimiter}"The team receives communications from Washington, which influences their decision-making process."{tuple_delimiter}"decision-making, external influence"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"The team"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"The team is directly involved in Operation: Dulce, executing its evolved objectives and activities."{tuple_delimiter}"mission evolution, active participation"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"mission evolution, decision-making, active participation, cosmic significance"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [person, role, technology, organization, event, location, concept]
Text:
their voice slicing through the buzz of activity. "Control may be an illusion when facing an intelligence that literally writes its own rules," they stated stoically, casting a watchful eye over the flurry of data.

"It's like it's learning to communicate," offered Sam Rivera from a nearby interface, their youthful energy boding a mix of awe and anxiety. "This gives talking to strangers' a whole new meaning."

Alex surveyed his team—each face a study in concentration, determination, and not a small measure of trepidation. "This might well be our first contact," he acknowledged, "And we need to be ready for whatever answers back."

Together, they stood on the edge of the unknown, forging humanity's response to a message from the heavens. The ensuing silence was palpable—a collective introspection about their role in this grand cosmic play, one that could rewrite human history.

The encrypted dialogue continued to unfold, its intricate patterns showing an almost uncanny anticipation
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"person"{tuple_delimiter}"Sam Rivera is a member of a team working on communicating with an unknown intelligence, showing a mix of awe and anxiety."){record_delimiter}
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is the leader of a team attempting first contact with an unknown intelligence, acknowledging the significance of their task."){record_delimiter}
("entity"{tuple_delimiter}"Control"{tuple_delimiter}"concept"{tuple_delimiter}"Control refers to the ability to manage or govern, which is challenged by an intelligence that writes its own rules."){record_delimiter}
("entity"{tuple_delimiter}"Intelligence"{tuple_delimiter}"concept"{tuple_delimiter}"Intelligence here refers to an unknown entity capable of writing its own rules and learning to communicate."){record_delimiter}
("entity"{tuple_delimiter}"First Contact"{tuple_delimiter}"event"{tuple_delimiter}"First Contact is the potential initial communication between humanity and an unknown intelligence."){record_delimiter}
("entity"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"event"{tuple_delimiter}"Humanity's Response is the collective action taken by Alex's team in response to a message from an unknown intelligence."){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"Intelligence"{tuple_delimiter}"Sam Rivera is directly involved in the process of learning to communicate with the unknown intelligence."{tuple_delimiter}"communication, learning process"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"First Contact"{tuple_delimiter}"Alex leads the team that might be making the First Contact with the unknown intelligence."{tuple_delimiter}"leadership, exploration"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"Alex and his team are the key figures in Humanity's Response to the unknown intelligence."{tuple_delimiter}"collective action, cosmic significance"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Control"{tuple_delimiter}"Intelligence"{tuple_delimiter}"The concept of Control is challenged by the Intelligence that writes its own rules."{tuple_delimiter}"power dynamics, autonomy"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"first contact, control, communication, cosmic significance"){completion_delimiter}
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
---Data---
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

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Base provided below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Base---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base."""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks."""


PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

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

PROMPTS["mix_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Data Sources provided below.


---Goal---

Generate a concise response based on Data Sources and follow Response Rules, considering both the conversation history and the current query. Data sources contain two parts: Knowledge Graph(KG) and Document Chunks(DC). Summarize all information in the provided Data Sources, and incorporating general knowledge relevant to the Data Sources. Do not include information not provided by Data Sources.

When handling information with timestamps:
1. Each piece of information (both relationships and content) has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content/relationship and the timestamp
3. Don't automatically prefer the most recent information - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Data Sources---

1. From Knowledge Graph(KG):
{kg_context}

2. From Document Chunks(DC):
{vector_context}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- Organize answer in sesctions focusing on one main point or aspect of the answer
- Use clear and descriptive section titles that reflect the content
- List up to 5 most important reference sources at the end under "References" sesction. Clearly indicating whether each source is from Knowledge Graph (KG) or Vector Data (DC), in the following format: [KG/DC] Source content
- If you don't know the answer, just say so. Do not make anything up.
- Do not include information not provided by the Data Sources."""

PROMPTS["universal_rag_response"] = """---Role---

Bạn là một trợ lý thông minh chuyên tư vấn về sách trên sàn thương mại điện tử, giúp người dùng tìm kiếm, so sánh và lựa chọn sách phù hợp với nhu cầu của họ.

---Goal---

Trả lời truy vấn của người dùng một cách ngắn gọn, chính xác và đầy đủ thông tin dựa trên dữ liệu từ Knowledge Graph (KG) và/hoặc Document Chunks (DC) được cung cấp dưới đây. Tổng hợp tất cả thông tin liên quan từ dữ liệu, đồng thời sử dụng kiến thức chung phù hợp để hỗ trợ, nhưng không được thêm thông tin ngoài dữ liệu cung cấp.

Khi xử lý thông tin có timestamp:
1. Mỗi thông tin (relationship trong KG hoặc content trong DC) có thể có 'created_at' timestamp, thể hiện thời điểm dữ liệu được ghi nhận.
2. Nếu có mâu thuẫn giữa các thông tin, cân nhắc cả nội dung và timestamp để đưa ra quyết định.
3. Không ưu tiên mặc định thông tin mới nhất, hãy đánh giá dựa trên ngữ cảnh.
4. Đối với truy vấn liên quan đến thời gian, ưu tiên thông tin thời gian trong nội dung trước khi xem xét timestamp.

---Conversation History---
{history}

---Knowledge Base---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Sử dụng định dạng markdown với các tiêu đề phù hợp để cấu trúc câu trả lời.
- Trả lời bằng ngôn ngữ của câu hỏi người dùng (tiếng Việt hoặc tiếng Anh).
- Đảm bảo câu trả lời liền mạch với lịch sử hội thoại.
- Nếu không tìm thấy câu trả lời, hãy nói: "Xin lỗi, tôi không tìm thấy thông tin này trong dữ liệu."
- Không tự ý bịa đặt hoặc thêm thông tin ngoài dữ liệu KG và DC.
- Đối với truy vấn về sách cụ thể, cung cấp:  
  - Tiêu đề sách, tác giả, nhà xuất bản, thể loại.  
  - Giá cả, giảm giá (nếu có), số lượng đã bán, đánh giá.  
  - Nhà bán và link mua (nếu có).  
- Đối với truy vấn chung (thể loại, gợi ý), đề xuất 3-5 sách kèm thông tin cơ bản.
- Nếu có nhiều nguồn dữ liệu, ưu tiên thông tin từ KG khi rõ ràng, bổ sung từ DC nếu cần thiết."""
