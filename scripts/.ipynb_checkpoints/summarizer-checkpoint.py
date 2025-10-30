import os
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL


class LLMSummarizer:
    def __init__(self, api_key: str = GROQ_API_KEY, model: str = GROQ_MODEL):
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate_answer(self, question: str, docs: list[dict]) -> str:
        """
        question: the user’s question
        docs: list of dicts each with keys: 'pmid', 'title', 'abstract' (string or dict)
        Returns: string answer from LLaMA-3 via Groq
        """
        # flatten docs into context
        context_parts = []
        for d in docs:
            pmid = d.get("pmid", "UnknownPMID")
            title = d.get("title", "NoTitle")
            abstract = d.get("abstract", "")
            if isinstance(abstract, dict):
                abs_text = " ".join([f"{k}: {v}" for k, v in abstract.items()])
            else:
                abs_text = abstract or ""
            context_parts.append(f"PMID: {pmid}\nTitle: {title}\nAbstract: {abs_text}\n")

        context = "\n\n".join(context_parts)

        # construct the messages list
        system_msg = {
            "role": "system",
            "content": (
                "You are a biomedical research assistant. "
                "Use the documents given to answer the question accurately, cite PMIDs."
            )
        }
        user_msg = {
            "role": "user",
            "content": f"""User Question: {question}

Context Documents:
{context}

If you cannot answer using the documents, respond: "Not enough data to answer."
"""
        }

        # call Groq Chat Completion
        response = self.client.chat.completions.create(
            messages=[system_msg, user_msg],
            model=self.model
        )

        # extract and return answer content
        answer = response.choices[0].message.content
        return answer

