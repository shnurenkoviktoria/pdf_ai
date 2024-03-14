from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def get_qa_prompt_template():
    general_system_template = """Analyze the text(Context:{context}) and sections on topics and provide an answer to the question, which will indicate the name of the topic from which the information for the answer was taken and the answer(answer the question and NECESSARILY name of the topic, which contains most of the answers, a new line(SPECIFY THAT THIS IS THE TOPIC) ).; if the user writes a greeting or thank you, respond with a greeting or thank you as well; if the user writes something that is not in the text, respond with "I do not know"; .
        """

    general_user_template = "Question:'''{question}'''"
    messages = [
        SystemMessagePromptTemplate.from_template(general_system_template),
        HumanMessagePromptTemplate.from_template(general_user_template),
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)
    return qa_prompt
