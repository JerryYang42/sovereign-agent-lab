"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking                                                                                                
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                  
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan                                                                                                         
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit                                                                                                                
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests  
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "deposit exceeds authorised limit"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit): 
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM correctly identified the out-of-scope request and informed the user that it could not handle it, redirecting them to the event organiser. It then offered to continue with the original booking task.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
In Exercise 2 Scenario 3, LangGraph also identified the out-of-scope request and redirected the user to authoritative sources. Both systems avoid hallucinating information, but CALM provides a more structured dialogue continuation by offering to resume the original task, and it escapes to a safe fallback response defined in flows.yml. LangGraph's response is more free-form and relies on the model's ability to stay on track, which can be less predictable.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
By changing the entry condition of `now.hour > 16 or (now.hour == 16 and now.minute >= 45)` to always-true, I forced the escalation path to trigger regardless of the actual time. I then ran the conversation and observed that it escalated with the correct reason related to the cutoff time.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

# Think about:
# - What does the LLM handle now that Python handled before?
# - What does Python STILL handle, and why (hint: business rules)?
# - Is there anything you trusted more in the old approach?

CALM_VS_OLD_RASA = """
CALM removes a lot of plumbing: the LLM now handles intent recognition and slot extraction directly from natural phrases like "about 160" without custom regex parsing. Python still owns the deterministic business checks (capacity, deposit limits, escalation reasons), which is exactly where strict control is needed. Compared with old Rasa, this is faster to build and easier to read, but I trust old rule-based pipelines slightly more for fully deterministic language interpretation in edge cases.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

# Be specific. What can the Rasa CALM agent NOT do that LangGraph could?
# Is that a feature or a limitation for the confirmation use case?
# Think about: can the CALM agent improvise a response it wasn't trained on?
# Can it call a tool that wasn't defined in flows.yml?
SETUP_COST_VALUE = """
The extra setup buys auditability and operational safety. In CALM, behavior is constrained by explicit flows and known actions, so the agent cannot freely improvise tasks or call arbitrary tools outside the flow definitions. LangGraph could dynamically choose tool sequences and explore broader requests at runtime, which is more flexible but less predictable. For booking confirmation, CALM's limits are mostly a feature: narrower scope, clearer escalation, and fewer hallucination paths. The trade-off is weaker adaptability to unexpected but reasonable user requests.
"""
