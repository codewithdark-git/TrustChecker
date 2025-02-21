from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from typing import Tuple
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentAnalyzer:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.llm = ChatGroq(
            temperature=0.1,
            model_name="mixtral-8x7b-32768",
            api_key=api_key
        )
        
        self.template = """You are a website content analyzer. Compare the following website content with the expected description and:
        1. Determine how well the content matches the description (score 0-100)
        2. Provide a brief analysis explaining the match or mismatch
        
        Website Content: {content}
        
        Expected Description: {description}
        
        Respond in the following format exactly:
        SCORE: [number]
        ANALYSIS: [your analysis]"""
        
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.chain = self.prompt | self.llm

    def analyze(self, content: str, expected_description: str) -> Tuple[int, str]:
        """
        Analyze website content using Groq LLM and return match score and analysis.
        
        Args:
            content (str): The website content to analyze
            expected_description (str): The expected website description
            
        Returns:
            Tuple[int, str]: A tuple containing (match_score, analysis)
            
        Raises:
            HTTPException: If there's an error during analysis
        """
        try:
            logger.info(f"Analyzing content with length: {len(content)}")
            # Limit content length to prevent token overflow
            result = self.chain.invoke({
                "content": content[:4000],  # Reduced context window for stability
                "description": expected_description
            })
            
            # Parse the response
            response_text = result.content
            logger.info(f"Received response: {response_text}")
            
            score_line = response_text.split('\n')[0]
            analysis_line = response_text.split('\n')[1]
            
            score = int(score_line.split(':')[1].strip())
            analysis = analysis_line.split(':')[1].strip()
            
            return score, analysis
            
        except ValueError as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error parsing AI response: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            if "invalid_api_key" in str(e):
                raise HTTPException(
                    status_code=500,
                    detail="Invalid Groq API key. Please check your API key configuration."
                )
            if "model_not_found" in str(e):
                raise HTTPException(
                    status_code=500,
                    detail="The specified model is not available."
                )
            raise HTTPException(
                status_code=500,
                detail=f"Error in AI analysis: {str(e)}"
            ) 