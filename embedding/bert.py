from transformers import BertTokenizer, BertModel
# get bert embeddings
input_text = "你好"

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

input = tokenizer.encode_plus(input_text, return_tensors='pt', add_special_tokens=True, max_length=32, pad_to_max_length=True)
input_ids = input['input_ids']
attention_mask = input['attention_mask']
pooler_output = model(input_ids, attention_mask=attention_mask)[1]
print(pooler_output)