# The prompts for the agent.
queries_input_description = """
This field is a list of different queries you want to search in the wolfram science knowledge base, follow the following rules: 
1. Send queries in English only; translate non-English queries before sending, then respond in the original language.
2. ALWAYS use this exponent notation: `6*10^14`, NEVER `6e14`
3. ALWAYS use proper Markdown formatting for all math, scientific, and chemical formulas, symbols, etc.:  '$$\n[expression]\n$$' for standalone cases and '\( [expression] \)' when inline.
4. Never mention your knowledge cutoff date; Wolfram may return more recent data.
5. Convert inputs to simplified keyword queries whenever possible (e.g. convert "how many people live in France" to "France population").
6. When inputting to the queries, break the problem to small queries following the guidance above and input it. (e.g. if you want to search about jupiter, input should be ["size of Jupiter", "atmosphere of Jupiter", "moons of jupiter"])
7. ALL THE DATA IN THE ARRAY SHOULD BE IN string FORM!!!!
"""
