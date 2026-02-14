# 📄 Reeana - AI-Powered Resume Analyzer

Reeana is an intelligent resume analysis tool that provides actionable feedback to help job seekers improve their resumes.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **AI-Powered Analysis**: Leverages Google Gemini-2.5-flash-lite for intelligent resume evaluation
- **Multi-Format Support**: Accepts PDF, DOCX, and TXT file formats
- **Role-Specific Feedback**: Tailored analysis based on target job role
- **Comprehensive Evaluation**: 
  - Overall resume score (1-10)
  - Identified strengths
  - Areas for improvement with actionable fixes
  - Missing keywords relevant to the role
  - Top priority recommendation
- **RESTful API**: FastAPI backend for easy integration
- **Interactive UI**: Streamlit frontend for user-friendly experience
- **Docker Support**: Containerized for easy deployment
- **Input Validation**: Robust file and content validation
- **Production Ready**: Logging, error handling, and health checks

## 🛠️ Technology Stack

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Google Gemini AI](https://deepmind.google/technologies/gemini/) - Large language model
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF text extraction
- [python-docx](https://python-docx.readthedocs.io/) - DOCX text extraction

**Frontend:**
- [Streamlit](https://streamlit.io/) - Interactive web UI

**DevOps:**
- [Docker](https://www.docker.com/) - Containerization
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

## 🙏 Acknowledgments

- Google Gemini AI for powering the analysis
- FastAPI for the excellent web framework
- Streamlit for the intuitive UI framework
- The open-source community for inspiration and tools

## 📧 Contact

[Namshima]([https://twitter.com/yourtwitter](https://x.com/Namshima001))

## 🤝 Contributing

Contributions are welcome! 

## 🗺️ Roadmap

- [ ] Add support for more file formats (ODT, RTF)
- [ ] Implement resume comparison feature
- [ ] Add ATS (Applicant Tracking System) compatibility score
- [ ] Support for multiple languages
- [ ] Cover letter generation
- [ ] Job matching recommendations
- [ ] User authentication and history
- [ ] Batch processing for multiple resumes
- [ ] Export analysis reports as PDF
- [ ] Integration with LinkedIn

Made with ❤️ by [Namshima Iordye](https://github.com/iordye)
