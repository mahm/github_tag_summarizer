from langchain.prompts.prompt import PromptTemplate


def overall_prompt():
    return PromptTemplate(
        input_variables=["desc", "text"],
        template=load_prompt("overall"),
    )


def each_ext_prompt():
    return PromptTemplate(
        input_variables=["desc", "text"],
        template=load_prompt("each_ext"),
    )


def each_file_prompt():
    return PromptTemplate(
        input_variables=["filename", "text"],
        template=load_prompt("each_file"),
    )


def load_prompt(prompt_name):
    with open(f"./src/prompts/{prompt_name}.prompt", "r") as f:
        return f.read()
