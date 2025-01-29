from setuptools import setup

setup(
    name="postman-collection-test-generator",
    version="1.0.1",
    author="Agnaldo Vilariano",
    author_email="agnaldo@example.com",
    description="Uma ferramenta para gerenciar projetos com templates pré-definidos.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vilariano/postman-collection-test-generator",  # Atualize com o link do seu repositório

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "gerenciador-projetos=postman-collection-test-generator.interface:criar_interface",
        ],
    },
)
