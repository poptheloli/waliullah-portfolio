import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        width, height = A4

        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(50, height - 36, "FINAL INTERNSHIP REPORT — WALIULLAH MAGSI | ATOM ACADEMY HYDERABAD")
            self.drawRightString(width - 50, height - 36, "IELL · UNIVERSITY OF SINDH")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(50, height - 42, width - 50, height - 42)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(50, 44, width - 50, 44)

        self.drawString(50, 32, "BS Applied Linguistics · Institute of English Language & Literature (IELL), University of Sindh, Jamshoro")
        self.drawRightString(width - 50, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def generate_report_pdf():
    pdf_filename = "Waliullah_Magsi_Final_Internship_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=0,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#065F46'),
        spaceAfter=12
    )

    institution_badge = ParagraphStyle(
        'InstBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E3A5F'),
        spaceAfter=6
    )

    sec_heading_style = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#0F2942'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.8,
        leading=14.5,
        textColor=colors.HexColor('#1E293B'),
        alignment=4,  # Justified
        spaceAfter=8
    )

    meta_lbl_style = ParagraphStyle(
        'MetaLbl',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155')
    )

    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Title block
    story.append(Paragraph("INSTITUTE OF ENGLISH LANGUAGE & LITERATURE (IELL) · UNIVERSITY OF SINDH, JAMSHORO", institution_badge))
    story.append(Paragraph("FINAL INTERNSHIP REPORT", title_style))
    story.append(Paragraph("Atom Academy, Hyderabad | Applied Linguistics | University of Sindh, Jamshoro", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#065F46"), spaceAfter=10, spaceBefore=0))

    # Metadata Table
    meta_data = [
        [
            Paragraph("<b>Candidate Name:</b>", meta_lbl_style), Paragraph("Waliullah Magsi", meta_val_style),
            Paragraph("<b>Degree Program:</b>", meta_lbl_style), Paragraph("BS Applied Linguistics", meta_val_style)
        ],
        [
            Paragraph("<b>Host Placement:</b>", meta_lbl_style), Paragraph("Atom Academy Hyderabad", meta_val_style),
            Paragraph("<b>Host Supervisor:</b>", meta_lbl_style), Paragraph("Sir Kashif Magsi (Teacher)", meta_val_style)
        ],
        [
            Paragraph("<b>Department:</b>", meta_lbl_style), Paragraph("IELL, University of Sindh", meta_val_style),
            Paragraph("<b>Academic Coordinator:</b>", meta_lbl_style), Paragraph("Madam Bakhtawar Jaleel (AL)", meta_val_style)
        ],
        [
            Paragraph("<b>Internship Duration:</b>", meta_lbl_style), Paragraph("60 Hours (26 Working Days)", meta_val_style),
            Paragraph("<b>Evaluation &amp; Score:</b>", meta_lbl_style), Paragraph("20 / 20 Marks (Grade: Outstanding)", meta_val_style)
        ]
    ]

    t = Table(meta_data, colWidths=[110, 140, 110, 135])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # SECTION 1
    story.append(Paragraph("1. Introduction", sec_heading_style))
    story.append(Paragraph(
        "My internship at Atom Academy, Hyderabad, formed an important practical component of my undergraduate studies in "
        "Applied Linguistics at the Institute of English Language and Literature, University of Sindh, Jamshoro. The principal objective "
        "was to connect linguistic knowledge acquired at university with the realities of teaching English to learners with different "
        "levels of proficiency. Rather than studying language only as an abstract system, I had the opportunity to plan lessons, explain "
        "grammatical structures, guide reading activities, develop vocabulary, and evaluate learning through classroom assessment.",
        body_style
    ))
    story.append(Paragraph(
        "I selected Atom Academy because its English-learning and university entry-test preparation activities offered an appropriate "
        "setting in which to practise teaching and observe students' language needs. My responsibilities included a Basic English "
        "Grammar course and preparation for the University of Sindh entry test. I expected to improve my teaching confidence, instructional "
        "communication, lesson planning, and ability to adapt linguistic concepts to accessible classroom explanations. The internship also "
        "provided an opportunity to examine how learners respond to different teaching strategies and how regular practice can support "
        "language development.",
        body_style
    ))

    # SECTION 2
    story.append(Paragraph("2. Organization Profile", sec_heading_style))
    story.append(Paragraph(
        "Atom Academy is an educational academy located in Hyderabad, Sindh. During my placement, its relevant instructional activities "
        "included Basic English Grammar teaching and preparation for the University of Sindh entry test. These programmes served learners "
        "who needed stronger foundational English skills as well as students preparing for an academic admission examination. My work was "
        "directly connected with these teaching and test-preparation activities.",
        body_style
    ))
    story.append(Paragraph(
        "The academy provided a practical environment for lessons, reading exercises, vocabulary practice, multiple-choice-question "
        "revision, and tests. I worked as an intern teacher under host supervision, preparing and delivering lessons and monitoring student "
        "progress. The educational purpose visible in my placement was to support students' learning and examination readiness. I have not "
        "included a formal mission statement, organizational chart, or departmental hierarchy because these were not available in the "
        "materials reviewed; those details should be confirmed with the academy before submission.",
        body_style
    ))

    # SECTION 3
    story.append(Paragraph("3. Job Description and Tasks Performed", sec_heading_style))
    story.append(Paragraph(
        "My principal responsibility was to teach English grammar while supporting students' reading, vocabulary development, and "
        "entry-test preparation. I prepared day-wise lesson plans with learning objectives, teaching materials, activities, and reflections. "
        "The initial orientation involved introducing the course and identifying students' starting levels through reading and basic grammar "
        "activities. This diagnostic approach helped me consider students' existing competence before progressing to more detailed instruction.",
        body_style
    ))
    story.append(Paragraph(
        "Throughout the internship, I taught grammatical categories and their functions, including pronouns and their types, verbs, "
        "adverbs and their types, and modal verbs. These topics were more than lists of definitions: they provided opportunities to relate "
        "<b>morphology</b>, which concerns word forms and grammatical categories, to <b>syntax</b>, which concerns how words function and "
        "combine in sentences. In explaining pronouns, for example, I could focus on reference and substitution within sentences; in verb "
        "lessons, I could discuss grammatical functions and sentence construction. Adverbs offered examples of how words modify actions "
        "and descriptions, while modal verbs provided a way to discuss meanings such as ability, possibility, and obligation. These are "
        "linguistic interpretations of the topics I taught, not a claim that every technical term was explicitly used in each lesson.",
        body_style
    ))
    story.append(Paragraph(
        "Reading passages and daily vocabulary activities formed another regular part of my work. Students read passages, practised "
        "pronunciation and fluency, and encountered new words in meaningful contexts. These activities supported reading comprehension, "
        "lexical development, and the connection between form and meaning. I observed that students' reading became more confident over "
        "time and that they increasingly remembered newly introduced vocabulary. Such observations were encouraging, although they were "
        "not based on standardized proficiency measurements.",
        body_style
    ))
    story.append(Paragraph(
        "Alongside grammar teaching, I conducted multiple-choice-question practice using past papers for the University of Sindh entry "
        "test. This was a distinct strand of the internship, rather than grammar practice alone. Students revised examination-style questions "
        "and became familiar with the format and demands of the test. I also administered a weekly grammar-course test and a mixed past-paper "
        "MCQ test. Toward the end of the placement, a comprehensive grammar test provided an opportunity to review overall learning; "
        "student performance was satisfactory. My tools included the whiteboard, markers, prepared reading passages, vocabulary exercises, "
        "lesson plans, past-paper questions, and assessment records. A WhatsApp group was also introduced for academic questions and "
        "class-related communication.",
        body_style
    ))

    # SECTION 4
    story.append(Paragraph("4. Learning Outcomes and Skills", sec_heading_style))
    story.append(Paragraph(
        "The internship strengthened my understanding of the relationship between linguistic theory and language pedagogy. At university, "
        "Applied Linguistics encourages students to examine language structure, language learning, and the social and educational contexts "
        "in which language is used. In the academy, these ideas became practical questions: How should a grammatical concept be explained? "
        "What examples will learners understand? How can a teacher identify confusion? Which activity gives students enough practice to improve?",
        body_style
    ))
    story.append(Paragraph(
        "One important learning outcome was the application of grammatical knowledge. Teaching parts of speech required grammatical "
        "competence and the ability to transform technical descriptions into clear explanations. The concepts of morphology and syntax helped "
        "me think systematically about word classes and sentence-level functions. Vocabulary activities drew attention to lexical competence, "
        "including the recognition, retention, and contextual use of words. Reading activities highlighted comprehension and fluency, showing "
        "that understanding a passage involves more than pronouncing individual words.",
        body_style
    ))
    story.append(Paragraph(
        "The experience also deepened my awareness of second-language learning. Students differed in confidence, prior knowledge, reading "
        "speed, and willingness to participate. This made learner-centred instruction and scaffolding especially relevant. I learned to move "
        "from simpler explanations and examples toward more demanding tasks, giving students opportunities to practise before expecting "
        "independent performance. Classroom interaction and question-and-answer exchanges supported communicative competence by encouraging "
        "students to use English to express understanding rather than merely memorize terminology.",
        body_style
    ))
    story.append(Paragraph(
        "Assessment was another major learning area. Initial activities had a diagnostic purpose, helping me recognize learner needs. Daily "
        "questions, vocabulary revision, and MCQ practice operated as formative assessment because they offered ongoing indications of what "
        "students understood and what needed reinforcement. Weekly tests and the final comprehensive test provided more formal checks on "
        "achievement. I learned that assessment should inform subsequent teaching, not simply produce marks. Reflective lesson planning "
        "helped me identify successful activities and areas needing adjustment.",
        body_style
    ))
    story.append(Paragraph(
        "In terms of professional skills, I developed instructional communication, time management, preparation, adaptability, and "
        "confidence in front of learners. I learned to organize a limited teaching period around grammar, reading, vocabulary, and entry-test "
        "practice without losing sight of the different objectives of each activity. Working within a supervised academy setting also "
        "improved my professional responsibility and my ability to respond constructively to students' questions. Maintaining an e-portfolio "
        "and internship records strengthened documentation and reflective writing, allowing me to connect daily experience with broader "
        "academic learning.",
        body_style
    ))

    # SECTION 5
    story.append(Paragraph("5. Challenges Faced", sec_heading_style))
    story.append(Paragraph(
        "A significant challenge was the gap between knowing a linguistic concept and teaching it effectively. A university-level "
        "explanation of syntax or grammatical classification may be accurate but too abstract for beginning learners. I addressed this by "
        "using straightforward language, familiar examples, repeated explanations, and practice questions. This helped me understand "
        "<b>pedagogical content knowledge</b>: a teacher must know not only the subject but also how to make it learnable.",
        body_style
    ))
    story.append(Paragraph(
        "Differences in student proficiency presented another challenge. Some learners could read and answer questions more confidently, "
        "while others needed additional guidance with passages and vocabulary. I responded through regular reading practice, repetition of "
        "new words, and opportunities for participation. Improvement was gradual, reminding me that language acquisition and literacy "
        "development require sustained exposure and meaningful practice rather than a single lecture.",
        body_style
    ))
    story.append(Paragraph(
        "Balancing the Basic English Grammar course with University of Sindh entry-test preparation also required careful planning. These "
        "activities overlapped in their broad aim of strengthening English but differed in immediate purpose: grammar lessons developed "
        "conceptual understanding, whereas past-paper MCQs developed familiarity with examination tasks. I kept both strands in the daily "
        "schedule and used separate exercises and tests when appropriate. Time constraints reinforced the importance of prioritizing "
        "objectives and maintaining continuity across sessions.",
        body_style
    ))
    story.append(Paragraph(
        "Finally, I learned that satisfactory test performance does not automatically demonstrate mastery of every aspect of language. "
        "Grammar tests and MCQs reveal useful information, but communicative ability, reading fluency, and long-term vocabulary retention "
        "also require observation over time. This realization encouraged a more balanced view of student progress and made my reflections "
        "more critical and evidence-conscious.",
        body_style
    ))

    # SECTION 6
    story.append(Paragraph("6. Conclusion", sec_heading_style))
    story.append(Paragraph(
        "My internship at Atom Academy, Hyderabad, was a valuable transition from undergraduate linguistic study to practical "
        "English-language teaching. Through lesson planning, grammar instruction, reading passages, vocabulary development, entry-test "
        "MCQ practice, and classroom assessment, I gained experience in adapting theoretical knowledge to actual learner needs. The "
        "placement showed me the practical relevance of morphology, syntax, grammatical and lexical competence, reading comprehension, "
        "communicative competence, scaffolding, and formative assessment.",
        body_style
    ))
    story.append(Paragraph(
        "Most importantly, I developed a stronger understanding of teaching as an ongoing cycle of planning, instruction, observation, "
        "assessment, and reflection. Students' increasing confidence in reading and their satisfactory performance in the final grammar "
        "assessment were encouraging outcomes, while the challenges reminded me that effective teaching requires patience and adjustment. "
        "The internship strengthened my communication, organization, reflective practice, and professional confidence. It also reinforced "
        "my interest in applying linguistic knowledge to improve English-language learning in educational settings.",
        body_style
    ))

    # Attestation Sign-off
    story.append(Spacer(1, 14))
    sign_table_data = [
        [
            Paragraph("<b>Candidate Signature:</b><br/><br/>__________________________<br/><b>Waliullah Magsi</b><br/>BS Applied Linguistics, University of Sindh", meta_val_style),
            Paragraph("<b>Host Supervisor Endorsement:</b><br/><br/>__________________________<br/><b>Sir Kashif Magsi</b><br/>Host Supervisor, Atom Academy Hyderabad", meta_val_style)
        ]
    ]
    st = Table(sign_table_data, colWidths=[245, 250])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(KeepTogether(st))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report PDF generated successfully:", pdf_filename)

if __name__ == "__main__":
    generate_report_pdf()
