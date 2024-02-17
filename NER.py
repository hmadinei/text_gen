import os
import replicate
import re

os.environ['REPLICATE_API_TOKEN'] = ''
token = os.environ.get('REPLICATE_API_TOKEN')


def request_llama(sentence):
    
    print("Start Requesting....")
    output = replicate.run(
        "meta/llama-2-70b-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48",
        input={
            "debug": False,
            "top_p": 1,
            "temperature": 0.1,
            "prompt":f"Given a sentence describing a laptop's specifications in Persian, your task is to identify and extract key information related to features such as RAM, brand, battery capacity, cache, CPU, GPU, and price. It's important to note that not every sentence will mention all these features. Some features may not be mentioned at all. For the features that are mentioned, normalize this information according to standard units and common expressions. For instance, if the price is mentioned as '50 تومن', normalize this to '50000000' (representing 50 million Tomans in numerical form). Similarly, ensure that any mentioned laptop brand is converted to a standardized brand name, like 'Asus'. Extract and normalize the information for each mentioned slot, and clearly indicate if a feature is not mentioned. the sentence is: {sentence}",
            "system_prompt": "You are an intelligent assistant with expertise in processing Persian text, specifically for extracting and normalizing laptop specifications. Your objective is to analyze provided sentences, identify key specifications, and normalize the information where applicable. It's crucial to recognize that not all features (RAM, brand, battery capacity, cache, CPU, GPU, price) will be mentioned in every query. For those that are mentioned, convert prices to numerical representation in Tomans, standardize brand names, and accurately identify and normalize other specifications. If a feature is not mentioned, acknowledge its absence. Approach each sentence as a unique request, focusing on extracting and normalizing only the information that is explicitly provided, ensuring accuracy and consistency in the data.",
            "max_new_tokens": 5000,
            "min_new_tokens": -1,
        }
    )
    
    print("Finish Requesting....")
    full_response = ""
    for item in output:
        full_response += item
        
    print(full_response)
    return full_response

def parse_request(llama_res):
    llama_res = llama_res.lower()
    
    # patterns
    slots = {
        'ram':re.compile(r"ram: (\d+)"),
        'brand':re.compile(r"brand: (\w+)\n"),
        'battery_capacity':re.compile(r"battery capacity: (.+?)\n"),
        'cache':re.compile(r"cache: (.+?)\n"),
        'cpu':re.compile(r"cpu: ([\w\s-]+)\n"),
        'gpu':re.compile(r"gpu: ([\w\s-]+)\n"),
        'price':re.compile(r"price: (\d+)\n"),
    }

    extracted_info = {}
    for key, slot in slots.items():
        if slot:
            match = slot.search(llama_res)
            extracted_info[key] = match.group(1) if match else None
        else:
            extracted_info[key] = None
           
    print(extracted_info)
    return extracted_info

    
    
if __name__=='__main__':
    llama_res = request_llama('سلام ببخشید میخواستم نظرتون رو در مورد Legion Slim 7 16IRH8 لنوو - Core i7-13700H RTX 4060 32GB 1TB بدونم که در رنج قیمتی خودش خوبه یا اگه در اون قیمت مدل بهتری هم هست بفرمایید  و این که کم بودن ضخامت باعث گرم شدن غیر عادی نمیشه که؟ ممنون')
    sentenses = parse_request(llama_res)