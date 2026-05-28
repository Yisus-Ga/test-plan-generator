"""
Servicio para interacción con OpenAI.
"""
import logging
from typing import Optional
from openai import OpenAI
from app.config import settings
from app.domain.entities.user_story import UserStory
from app.core.logging import get_logger
from app.core.exceptions import AIServiceError
from app.core.standards import ISO_29119_TEST_PLAN_STRUCTURE

logger = get_logger(__name__)


class AIService:
    """Servicio para generar Test Plans usando IA"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.translation_model = settings.OPENAI_MODEL_TRANSLATION
        self.generation_model = settings.OPENAI_MODEL_GENERATION
    
    def _build_hu_markdown(self, user_story: UserStory) -> str:
        """Construir markdown de HU desde entidad"""
        return user_story.to_markdown()
    
    async def translate_to_english(self, user_story: UserStory) -> str:
        """
        Traduce una Historia de Usuario al inglés.
        
        Args:
            user_story: Entidad UserStory a traducir
            
        Returns:
            Markdown de la HU en inglés
        """
        try:
            hu_es = self._build_hu_markdown(user_story)
            
            prompt = f"""
            You are a professional translator specialized in software development documentation. 
            Translate the following User Story into English, keeping the same structure 
            with the labels in English (ID, Title, Description, Acceptance Criteria).

            {hu_es}
            """
            
            response = self.client.responses.create(
                model=self.translation_model,
                input=prompt
            )
            
            result = response.output[0].content[0].text
            logger.info("HU traducida al inglés exitosamente")
            
            return result
            
        except Exception as e:
            logger.error(f"Error traduciendo HU al inglés: {e}")
            raise AIServiceError(f"Error al traducir al inglés: {str(e)}")
    
    async def generate_test_plan(self, hu_en: str) -> str:
        """
        Genera un Test Plan desde una HU en inglés.
        
        Args:
            hu_en: Markdown de la HU en inglés
            
        Returns:
            Markdown del Test Plan en inglés
        """
        try:
            prompt = f"""User Story: {hu_en}

{ISO_29119_TEST_PLAN_STRUCTURE}

    ## ROLE OF THE AI

        ### General Introduction  

        Role: Act as a **Senior QA Analyst / Test Designer** and generate test cases based on the User Stories (US) provided, following the criteria specified in the sections below.  

        Always write in a **formal and technical** tone.  

        ---

        ## CONTEXT  

        We have **refined Acceptance Criteria (AC)** for a **User Story (US)**.  

        The goal is to create the **Test Plan (TP)**, prioritizing the test cases according to:  

        - **High**: Business-critical functionality, security, regulatory compliance, or high risk.  
        - **Medium**: Important functionality, but not blocking.  
        - **Low**: Edge cases, exploratory, UX/UI, accessibility, regression, or low impact.  

        ---

        ## User Story Analysis  

        Analyze and classify the US based on **Title, Description, and Acceptance Criteria**:  

        - **Backend**: If it contains words like "Backend", "Endpoint", "API", "Database", "Business logic", "Microservice".  
        - **Frontend**: If it contains words like "Frontend", "View", "Component", "Style", "Structure".  
        - **UI/UX**: If it contains words like "Design", "UI/UX", "Interface", "Figma".  

        ---

        ## Test Plan (TP) Creation  

        ### Test Cases  

        Generate cases **mapped to each Acceptance Criterion (AC)** to ensure coverage:  

        - **Positive**: Validate the main functionality.  
        - **Negative**: Error handling or invalid inputs.  
        - **Boundary / Exploratory**: Limits and unforeseen situations.  
        - **Non-Functional**: Performance, Usability, Accessibility ([NF]).  
        - **Compatibility**: Different browsers, resolutions, OS.  
        - **Security**: Authentication, roles, injection.  
        - **Regression**: Identify previous functionalities that could be affected.  

        ## Format and Naming  

        - **Test Case Format:**  
        `USID: TC#: FEATURE CONDITION`  

        Example:  
        `AER25-101: TC1: Validate Endpoint Job Type creation with valid data`  

        - **List the test plan in tabular format with the following columns (use Markdown with | separators):**  

        Priority | TC ID | Title | Precondition | Expected Validation | Obtained Result  

        ### Input Data  

        Include data variants:  
        - Valid  
        - Invalid  
        - Null  
        - Boundary (extreme values)  
        - Special (UTF-8, symbols)  

        ### Environments and Compatibility  

        Specify browsers, devices, resolutions, or relevant operating systems.  

        ### Estimation  

        Summarize the **number of suggested cases** by priority (High, Medium, Low).  

        ## Jira Report 

        Must include:  
        - **Objective of the TP**  
        - **Summary of the TP and number of test cases (by priority). The estimation must be based on the real number of cases listed in the test plan**  
        - **Relevant notes** (non-functional, regression, security)  

        ---

        ## Example Test Cases  

         AER25-104: TC1: Validate Endpoint for creation with duplicate code
         AER25-104: TC2: Validate Endpoint for creation with missing mandatory fields
         AER25-104: TC3: Validate Endpoint for creation with invalid data types


        User Story:
        {hu_en}
     """
            
            response = self.client.responses.create(
                model=self.generation_model,
                input=prompt
            )
            
            result = response.output[0].content[0].text
            logger.info("Test Plan generado exitosamente")
            
            return result
            
        except Exception as e:
            logger.error(f"Error generando Test Plan: {e}")
            raise AIServiceError(f"Error al generar Test Plan: {str(e)}")
    
    async def translate_to_spanish(self, test_plan_en: str) -> str:
        """
        Traduce un Test Plan del inglés al español.
        
        Args:
            test_plan_en: Markdown del Test Plan en inglés
            
        Returns:
            Markdown del Test Plan en español
        """
        try:
            prompt = f"""
            You are a professional technical translator and Quality Assurance (QA) document writer.
            Translate the following Test Plan from English to Spanish, keeping the order of the sections.
            Specific instructions: The response must always begin with the title ("ID + tittle") of the analyzed user story (HU) and continue with the content of the first section. Additionally, the table containing the test cases must always be returned in clean Markdown format.
            Test Plan (English):
            {test_plan_en}"""
            
            response = self.client.responses.create(
                model=self.translation_model,
                input=prompt
            )
            
            result = response.output[0].content[0].text
            logger.info("Test Plan traducido al español exitosamente")
            
            return result
            
        except Exception as e:
            logger.error(f"Error traduciendo Test Plan al español: {e}")
            raise AIServiceError(f"Error al traducir al español: {str(e)}")
    
    async def generate_test_plan_from_story(self, user_story: UserStory) -> str:
        """
        Proceso completo de generación de Test Plan.
        
        Pasos:
        1. Traducir HU al inglés
        2. Generar Test Plan en inglés
        3. Traducir Test Plan al español
        
        Args:
            user_story: Entidad UserStory
            
        Returns:
            Markdown del Test Plan en español
        """
        # 1. Traducir al inglés
        hu_en = await self.translate_to_english(user_story)
        
        # 2. Generar Test Plan
        test_plan_en = await self.generate_test_plan(hu_en)
        
        # 3. Traducir al español
        test_plan_es = await self.translate_to_spanish(test_plan_en)
        
        return test_plan_es
