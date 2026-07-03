import json
import pandas as pd

class fewShotPosts:
    def __init__(self,file_path="Your_Path"):
        self.df = pd.DataFrame()
        self.unique_tags = []
        self.load_posts(file_path)

    def load_posts(self,file_path):
        with open(file_path, encoding= "utf-8") as f:
            posts= json.load(f)
            self.df=pd.json_normalize(posts)
            
            # 1. Compute length
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)
            
            # --- THE FIX ---
            # 2. Inject default language if it is missing from the JSON
            if 'language' not in self.df.columns:
                self.df['language'] = "English"
            # ---------------
            
            # 3. Extract unique tags
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = list(set(all_tags))

    def categorize_length(self, line_count):
        if line_count < 5:
            return "short"
        elif 5 <= line_count <= 10:
            return "medium"
        else:
            return "long"        
       
    def get_tags(self):
        return self.unique_tags
    
    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['length'] == length) &
            (self.df['language'] == language) &
            (self.df['tags'].apply(lambda x: tag in x))
        ]
        return df_filtered.to_dict(orient='records')

if __name__ == "__main__":
    few_shot = fewShotPosts()
    posts= few_shot.get_filtered_posts(length="medium", language="English", tag="Data Thinking")
    # ADD THIS: Print the filtered posts nicely formatted
    print(json.dumps(posts, indent=4, ensure_ascii=False))
