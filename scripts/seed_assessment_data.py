"""
One-off script to seed sample tests + questions across several languages/
domains, so you have real, demo-ready content for the assessment flow and
the language-score summary.

Run once from the portal-fastapi folder with:
    python -m scripts.seed_assessment_data

Safe to re-run — it skips creating a test if one with the same title
already exists. To REPLACE an existing test's questions (e.g. after
editing this file), delete that test first via the database, or add a
--force flag yourself if you want that convenience later.

NOTE: if your app/db/session.py exposes the session factory under a
different name than `SessionLocal`, adjust the import below to match.
"""

from app.db.session import SessionLocal
from app.models.models import Test, Question


def q(text, options, correct_option):
    return {"text": text, "options": options, "correct_option": correct_option}


SAMPLE_TESTS = [
    {
        "title": "Python Basics",
        "discipline": "IT",
        "category": "Programming",
        "subcategory": "Python",
        "topic": None,
        "duration_minutes": 25,
        "passing_percent": 40,
        "questions": [
            q("What does len([1, 2, 3]) return?", ["2", "3", "4", "Error"], 1),
            q("Which keyword defines a function in Python?", ["func", "def", "function", "lambda"], 1),
            q("What is the output of 3 // 2 in Python?", ["1.5", "1", "2", "Error"], 1),
            q("Which of these is mutable?", ["tuple", "string", "list", "int"], 2),
            q("What does type([]) return?", ["<class 'array'>", "<class 'list'>", "<class 'tuple'>", "<class 'dict'>"], 1),
            q("Which keyword is used to define a class?", ["object", "class", "struct", "define"], 1),
            q("range(5) generates which sequence?", ["1 to 5", "0 to 4", "0 to 5", "1 to 4"], 1),
            q("Which method adds an item to the end of a list?", ["add()", "push()", "append()", "insert()"], 2),
            q("Which construct is used for exception handling?", ["try/except", "catch/throw", "on error", "handle/rescue"], 0),
            q("Which operator is used for exponentiation?", ["^", "**", "exp()", "pow"], 1),
            q("What is bool(0) in Python?", ["True", "False", "0", "None"], 1),
            q("Which brackets define a dictionary?", ["[]", "()", "{}", "<>"], 2),
            q("Which method converts a string to lowercase?", ["toLower()", "lower()", "lowercase()", "downcase()"], 1),
            q("A lambda in Python is a(n):", ["Named function", "Anonymous function", "Class method", "Loop"], 1),
            q("Which module provides regular expressions?", ["regex", "re", "pyregex", "restring"], 1),
            q("What does 'self' refer to inside a class method?", ["The class itself", "The instance", "A global variable", "Nothing, it's optional"], 1),
            q("Which of these is immutable?", ["list", "dict", "set", "tuple"], 3),
            q("What is the standard file extension for Python files?", [".py", ".pt", ".pyt", ".python"], 0),
            q("Which function reads input from the user?", ["read()", "scan()", "input()", "get()"], 2),
            q("What does PEP stand for?", ["Python Extension Package", "Python Enhancement Proposal", "Python Execution Plan", "Public Environment Package"], 1),
        ],
    },
    {
        "title": "Java Fundamentals",
        "discipline": "IT",
        "category": "Programming",
        "subcategory": "Java",
        "topic": None,
        "duration_minutes": 25,
        "passing_percent": 40,
        "questions": [
            q("Which method is the entry point of a Java program?", ["start()", "main()", "run()", "init()"], 1),
            q("Which keyword is used to inherit a class?", ["implements", "inherits", "extends", "super"], 2),
            q("What is the default value of a boolean field?", ["true", "false", "0", "null"], 1),
            q("Which keyword creates a new object?", ["make", "new", "create", "object"], 1),
            q("Which of these is NOT a Java primitive type?", ["int", "float", "String", "boolean"], 2),
            q("Which keyword prevents a class from being subclassed?", ["static", "final", "const", "sealed"], 1),
            q("Which collection type does not allow duplicate elements?", ["List", "Set", "Map", "Array"], 1),
            q("What does JVM stand for?", ["Java Verified Module", "Java Virtual Machine", "Java Variable Manager", "Java Visual Model"], 1),
            q("Which method runs automatically when an object is created?", ["init()", "constructor", "main()", "onCreate()"], 1),
            q("Which keyword starts an exception-handling block?", ["try", "catch", "throw", "except"], 0),
            q("Which access modifier restricts access to only within the class?", ["public", "protected", "private", "default"], 2),
            q("Which construct allows a class to implement multiple contracts?", ["Multiple classes", "Interfaces", "Abstract classes", "Packages"], 1),
            q("Which keyword defines a constant field?", ["const", "static", "final", "readonly"], 2),
            q("How many bytes does an int typically occupy in Java?", ["2", "4", "8", "1"], 1),
            q("Which package contains the Scanner class?", ["java.io", "java.util", "java.lang", "java.scan"], 1),
            q("Which method checks value equality between two objects?", ["==", "equals()", "compareTo()", "same()"], 1),
            q("Which class is used to create a new thread?", ["Runnable", "Thread", "Process", "Task"], 1),
            q("Method overloading means:", ["Same name, same parameters", "Same name, different parameters", "Different name, same parameters", "Overriding a parent method"], 1),
            q("Which keyword is used to implement an interface?", ["extends", "implements", "inherits", "uses"], 1),
            q("Which of these is a checked exception?", ["NullPointerException", "ArithmeticException", "IOException", "ArrayIndexOutOfBoundsException"], 2),
        ],
    },
    {
        "title": "C++ Fundamentals",
        "discipline": "IT",
        "category": "Programming",
        "subcategory": "C++",
        "topic": None,
        "duration_minutes": 25,
        "passing_percent": 40,
        "questions": [
            q("Which header is required to use cout?", ["<stdio.h>", "<iostream>", "<conio.h>", "<string>"], 1),
            q("Which symbol declares a pointer?", ["&", "*", "#", "@"], 1),
            q("Which keyword defines a class?", ["struct", "class", "object", "type"], 1),
            q("What is the default access specifier in a class?", ["public", "protected", "private", "internal"], 2),
            q("Which operator is used for scope resolution?", ["->", "::", ".", "::>"], 1),
            q("Which function is the entry point of a C++ program?", ["start()", "main()", "run()", "init()"], 1),
            q("Which keyword allocates memory dynamically?", ["malloc", "alloc", "new", "create"], 2),
            q("Which keyword frees dynamically allocated memory?", ["free", "delete", "clear", "remove"], 1),
            q("Which symbol is used to specify inheritance from a base class?", [":", "::", "->", "extends"], 0),
            q("What does STL stand for?", ["Standard Type Library", "Standard Template Library", "System Template Layer", "Static Type Library"], 1),
            q("Which keyword prevents a function from modifying member variables?", ["static", "const", "final", "readonly"], 1),
            q("Which operator accesses a member through a pointer?", [".", "->", "::", "*"], 1),
            q("Which STL container stores key-value pairs?", ["vector", "list", "map", "set"], 2),
            q("A constructor is:", ["Called when an object is destroyed", "Called when an object is created", "A static method", "Optional in every class"], 1),
            q("Defining multiple functions with the same name but different parameters is called:", ["Function overriding", "Function overloading", "Polymorphism only", "Templating"], 1),
            q("Which of these is NOT a primitive data type in C++?", ["int", "char", "float", "string"], 3),
            q("What is the typical size of an int in C++?", ["2 bytes", "4 bytes", "8 bytes", "16 bytes"], 1),
            q("Which keyword brings a namespace into scope?", ["import", "using", "include", "namespace"], 1),
            q("Which of the following is a valid single-line comment in C++?", ["<!-- comment -->", "# comment", "// comment", "' comment"], 2),
            q("Which keyword allows a derived class to override a base class method?", ["override", "virtual", "abstract", "final"], 1),
        ],
    },
    {
        "title": "Data Structures & Algorithms",
        "discipline": "IT",
        "category": "Programming",
        "subcategory": "DSA",
        "topic": None,
        "duration_minutes": 30,
        "passing_percent": 40,
        "questions": [
            q("What is the time complexity of binary search?", ["O(n)", "O(log n)", "O(n log n)", "O(1)"], 1),
            q("Which data structure follows FIFO order?", ["Stack", "Queue", "Tree", "Graph"], 1),
            q("Which data structure follows LIFO order?", ["Queue", "Stack", "Linked list", "Heap"], 1),
            q("What is the time complexity of accessing an array element by index?", ["O(n)", "O(log n)", "O(1)", "O(n^2)"], 2),
            q("Which sorting algorithm generally has the best average-case time complexity?", ["Bubble sort", "Insertion sort", "Quicksort", "Selection sort"], 2),
            q("Which data structure is typically used to implement BFS?", ["Stack", "Queue", "Heap", "Array"], 1),
            q("Which data structure is typically used to implement DFS (iteratively)?", ["Queue", "Stack", "Heap", "Hash table"], 1),
            q("What is the time complexity of inserting at the head of a linked list?", ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 0),
            q("A linear collection where each element points to the next is called a:", ["Array", "Linked list", "Tree", "Graph"], 1),
            q("What is the worst-case time complexity of quicksort?", ["O(n log n)", "O(n)", "O(n^2)", "O(log n)"], 2),
            q("Which structure is used to manage function calls, including recursion?", ["Queue", "Stack (call stack)", "Heap", "Linked list"], 1),
            q("In a binary search tree, for any node:", ["Left < node < right", "Left > node > right", "All children are equal", "There is no ordering rule"], 0),
            q("What is the worst-case time complexity of bubble sort?", ["O(n)", "O(n log n)", "O(n^2)", "O(1)"], 2),
            q("Which data structure is commonly used to efficiently pick the minimum element repeatedly (e.g. Dijkstra's algorithm)?", ["Stack", "Queue", "Min-heap / priority queue", "Linked list"], 2),
            q("A hash table is primarily used for:", ["Ordered traversal", "Fast key-based lookup", "Sorting data", "Graph traversal"], 1),
            q("What is the time complexity of merge sort?", ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"], 1),
            q("A connected graph with no cycles is called a:", ["Tree", "Queue", "Heap", "Hash map"], 0),
            q("For a balanced binary tree with n nodes, the height is approximately:", ["O(n)", "O(log n)", "O(n^2)", "O(1)"], 1),
            q("Which traversal visits the root, then left subtree, then right subtree?", ["Inorder", "Postorder", "Preorder", "Level-order"], 2),
            q("What is the typical space complexity of computing Fibonacci with memoization?", ["O(1)", "O(n)", "O(2^n)", "O(n^2)"], 1),
        ],
    },
    {
        "title": "Financial Accounting Basics",
        "discipline": "Commerce",
        "category": "Finance",
        "subcategory": "Accounting",
        "topic": None,
        "duration_minutes": 20,
        "passing_percent": 40,
        "questions": [
            q("Which statement shows a company's profit or loss over a period?", ["Balance Sheet", "Income Statement", "Cash Flow Statement", "Trial Balance"], 1),
            q("Assets = Liabilities + ?", ["Revenue", "Expenses", "Equity", "Debt"], 2),
            q("Depreciation is recorded on which type of asset?", ["Current assets", "Fixed assets", "Intangible liabilities", "Equity"], 1),
            q("Which account normally has a debit balance?", ["Revenue", "Liabilities", "Expenses", "Equity"], 2),
            q("Which financial statement shows a company's assets, liabilities, and equity at a point in time?", ["Income Statement", "Balance Sheet", "Cash Flow Statement", "Ledger"], 1),
            q("What does GAAP stand for?", ["Generally Accepted Accounting Principles", "General Accounting and Auditing Practices", "Government Approved Accounting Policy", "Global Accounting Assessment Process"], 0),
            q("Which entry increases an asset account?", ["Credit", "Debit", "Neither", "Both equally"], 1),
            q("What is the accounting equation used for?", ["Calculating tax", "Ensuring the books balance", "Setting prices", "Forecasting sales"], 1),
            q("Which document records a company's day-to-day transactions first?", ["Ledger", "Trial balance", "Journal", "Balance sheet"], 2),
            q("Accounts payable is classified as a:", ["Current asset", "Current liability", "Long-term asset", "Equity"], 1),
        ],
    },
    {
        "title": "Human Anatomy Basics",
        "discipline": "Medical",
        "category": "Biology",
        "subcategory": "Anatomy",
        "topic": None,
        "duration_minutes": 20,
        "passing_percent": 40,
        "questions": [
            q("How many chambers does the human heart have?", ["2", "3", "4", "5"], 2),
            q("Which organ is primarily responsible for filtering blood?", ["Liver", "Kidney", "Spleen", "Pancreas"], 1),
            q("The femur is located in which part of the body?", ["Arm", "Skull", "Leg", "Spine"], 2),
            q("Which system is responsible for transporting oxygen in the body?", ["Digestive system", "Respiratory system", "Circulatory system", "Nervous system"], 2),
            q("How many bones are in the adult human body?", ["186", "206", "226", "246"], 1),
            q("Which organ produces insulin?", ["Liver", "Pancreas", "Kidney", "Stomach"], 1),
            q("The largest organ in the human body is the:", ["Liver", "Brain", "Skin", "Lungs"], 2),
            q("Which part of the brain controls balance and coordination?", ["Cerebrum", "Cerebellum", "Medulla", "Hypothalamus"], 1),
            q("Which blood cells are primarily responsible for fighting infection?", ["Red blood cells", "White blood cells", "Platelets", "Plasma cells"], 1),
            q("The trachea is part of which system?", ["Digestive", "Respiratory", "Nervous", "Skeletal"], 1),
        ],
    },
    {
        "title": "Human Physiology Basics",
        "discipline": "Medical",
        "category": "Biology",
        "subcategory": "Physiology",
        "topic": None,
        "duration_minutes": 20,
        "passing_percent": 40,
        "questions": [
            q("What is the normal resting heart rate range for adults?", ["30-50 bpm", "60-100 bpm", "110-140 bpm", "150-180 bpm"], 1),
            q("What is the normal average body temperature?", ["35°C", "37°C", "39°C", "41°C"], 1),
            q("Which organ regulates blood sugar via insulin and glucagon?", ["Liver", "Pancreas", "Kidney", "Spleen"], 1),
            q("Which gas is exchanged for oxygen in the alveoli?", ["Nitrogen", "Carbon dioxide", "Hydrogen", "Helium"], 1),
            q("Which hormone helps regulate blood calcium levels?", ["Insulin", "Parathyroid hormone", "Adrenaline", "Thyroxine"], 1),
            q("What is the normal pH range of human blood?", ["6.0-6.5", "7.0-7.2", "7.35-7.45", "8.0-8.5"], 2),
            q("Which chamber of the heart pumps blood to the lungs?", ["Left atrium", "Left ventricle", "Right atrium", "Right ventricle"], 3),
            q("What is the functional unit of the kidney called?", ["Neuron", "Nephron", "Alveolus", "Villus"], 1),
            q("Which neurotransmitter triggers muscle contraction at the neuromuscular junction?", ["Dopamine", "Serotonin", "Acetylcholine", "GABA"], 2),
            q("Which process describes the body maintaining a stable internal environment?", ["Metabolism", "Homeostasis", "Respiration", "Digestion"], 1),
        ],
    },
    {
        "title": "Biochemistry Basics",
        "discipline": "Medical",
        "category": "Biology",
        "subcategory": "Biochemistry",
        "topic": None,
        "duration_minutes": 20,
        "passing_percent": 40,
        "questions": [
            q("What is the basic building block of a protein?", ["Nucleotide", "Amino acid", "Fatty acid", "Monosaccharide"], 1),
            q("Which molecule stores genetic information?", ["RNA only", "DNA", "ATP", "Protein"], 1),
            q("What is the primary energy currency of the cell?", ["Glucose", "ATP", "NADH", "Insulin"], 1),
            q("Which enzyme breaks down starch into simpler sugars?", ["Lipase", "Amylase", "Protease", "Catalase"], 1),
            q("What are the building blocks of nucleic acids called?", ["Amino acids", "Fatty acids", "Nucleotides", "Peptides"], 2),
            q("A deficiency of which vitamin causes scurvy?", ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D"], 2),
            q("What is the process of breaking down glucose for energy called?", ["Photosynthesis", "Glycolysis", "Transcription", "Translation"], 1),
            q("Which organelle is the main site of cellular respiration?", ["Nucleus", "Ribosome", "Mitochondria", "Golgi apparatus"], 2),
            q("What type of bond links amino acids together in a protein?", ["Hydrogen bond", "Ionic bond", "Peptide bond", "Glycosidic bond"], 2),
            q("Which macromolecule is the main component of cell membranes?", ["Carbohydrates", "Phospholipids", "Nucleic acids", "Proteins only"], 1),
        ],
    },
    {
        "title": "Pharmacology Basics",
        "discipline": "Medical",
        "category": "Medicine",
        "subcategory": "Pharmacology",
        "topic": None,
        "duration_minutes": 20,
        "passing_percent": 40,
        "questions": [
            q("Pharmacokinetics studies:", ["How drugs affect the body's receptors", "How the body absorbs, distributes, metabolizes, and excretes a drug", "Drug pricing", "Drug manufacturing"], 1),
            q("Pharmacodynamics studies:", ["Drug effects on the body", "Drug packaging", "Drug storage temperature", "Drug marketing"], 0),
            q("Which route of administration typically has the fastest onset of action?", ["Oral", "Intramuscular", "Intravenous", "Topical"], 2),
            q("A drug's \"half-life\" refers to:", ["Time to take full effect", "Time for its concentration in the body to reduce by half", "Time until it expires", "Time to be manufactured"], 1),
            q("Paracetamol is commonly used as a(n):", ["Antibiotic", "Analgesic/antipyretic", "Antihistamine", "Antiviral"], 1),
            q("Antibiotics are used to treat infections caused by:", ["Viruses", "Bacteria", "Fungi only", "Prions"], 1),
            q("An antagonist drug:", ["Activates a receptor", "Blocks a receptor without activating it", "Has no effect on receptors", "Always cures disease"], 1),
            q("Which organ is primarily responsible for metabolizing most drugs?", ["Kidney", "Liver", "Lungs", "Spleen"], 1),
            q("Which organ is primarily responsible for excreting most drugs and their metabolites?", ["Liver", "Kidney", "Skin", "Stomach"], 1),
            q("What does \"OTC\" mean in pharmacology?", ["On-the-counter prescription", "Over-the-counter (no prescription needed)", "Optional trial compound", "Official test compound"], 1),
        ],
    },
    {
        "title": "General Pathology Basics",
        "discipline": "Medical",
        "category": "Medicine",
        "subcategory": "Pathology",
        "topic": None,
        "duration_minutes": 20,
        "passing_percent": 40,
        "questions": [
            q("Inflammation is primarily the body's response to:", ["Aging", "Injury or infection", "Sleep", "Exercise"], 1),
            q("Which white blood cell count typically rises during a bacterial infection?", ["Lymphocytes only", "Neutrophils", "Platelets", "Red blood cells"], 1),
            q("A benign tumor is best described as:", ["Cancerous and spreads", "Non-cancerous and does not spread", "Always fatal", "A type of infection"], 1),
            q("A malignant tumor is best described as:", ["Non-cancerous", "Cancerous, capable of spreading (metastasis)", "Always small", "A vitamin deficiency"], 1),
            q("The term for cell death due to injury or disease is:", ["Apoptosis", "Necrosis", "Mitosis", "Meiosis"], 1),
            q("Edema refers to:", ["Low blood pressure", "Swelling due to fluid accumulation", "High fever", "Low blood sugar"], 1),
            q("Which test reflects average blood sugar levels over about 3 months?", ["Fasting glucose", "HbA1c", "Urinalysis", "CBC"], 1),
            q("Jaundice is primarily caused by excess:", ["Glucose", "Bilirubin", "Cholesterol", "Sodium"], 1),
            q("Anemia is characterized by:", ["Excess white blood cells", "Low red blood cell count / low hemoglobin", "High blood pressure", "Excess platelets"], 1),
            q("Programmed cell death, a normal part of development, is called:", ["Necrosis", "Apoptosis", "Metastasis", "Ischemia"], 1),
        ],
    },
    {
        "title": "Microbiology Basics",
        "discipline": "Medical",
        "category": "Medicine",
        "subcategory": "Microbiology",
        "topic": None,
        "duration_minutes": 20,
        "passing_percent": 40,
        "questions": [
            q("Which microorganism causes tuberculosis?", ["Escherichia coli", "Mycobacterium tuberculosis", "Staphylococcus aureus", "Plasmodium falciparum"], 1),
            q("What is generally considered the smallest infectious agent?", ["Bacteria", "Fungi", "Virus", "Protozoa"], 2),
            q("Which staining technique is commonly used to classify bacteria?", ["PCR", "Gram stain", "ELISA", "Karyotyping"], 1),
            q("A vaccine is primarily designed to:", ["Kill existing infections directly", "Stimulate immunity against a specific pathogen", "Replace antibiotics", "Reduce fever only"], 1),
            q("Malaria is caused by which type of organism?", ["Bacteria", "Virus", "Parasite (Plasmodium)", "Fungus"], 2),
            q("An antibiotic works by:", ["Killing or inhibiting bacteria", "Killing viruses", "Boosting vitamin levels", "Reducing blood pressure"], 0),
            q("A mutually beneficial relationship between two organisms is called:", ["Parasitism", "Symbiosis (mutualism)", "Predation", "Competition"], 1),
            q("Which structure allows many bacteria to move?", ["Cell wall", "Flagella", "Ribosome", "Capsule"], 1),
            q("A pathogen is best defined as:", ["Any living cell", "A disease-causing organism", "A type of antibody", "A vaccine ingredient"], 1),
            q("Immunity gained through vaccination is called:", ["Passive immunity", "Innate immunity", "Acquired (active) immunity", "Natural immunity only"], 2),
        ],
    },
]


def seed():
    db = SessionLocal()
    try:
        created = 0
        for test_data in SAMPLE_TESTS:
            exists = db.query(Test).filter(Test.title == test_data["title"]).first()
            if exists:
                print(f"Skipping (already exists): {test_data['title']}")
                continue

            test = Test(
                title=test_data["title"],
                discipline=test_data["discipline"],
                category=test_data["category"],
                subcategory=test_data["subcategory"],
                topic=test_data["topic"],
                duration_minutes=test_data["duration_minutes"],
                passing_percent=test_data["passing_percent"],
            )
            db.add(test)
            db.flush()

            for i, ques in enumerate(test_data["questions"]):
                db.add(Question(
                    test_id=test.id,
                    text=ques["text"],
                    options=ques["options"],
                    correct_option=ques["correct_option"],
                    marks=1,
                    order_index=i,
                ))

            created += 1
            print(f"Created: {test_data['title']} ({len(test_data['questions'])} questions)")

        db.commit()
        print(f"\nDone. {created} test(s) created.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()