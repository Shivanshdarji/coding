import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime


class MentalHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mindful Companion")
        self.root.geometry("800x600")
        self.root.configure(bg='#decaf3')

        # Configure notebook style
        style = ttk.Style()
        style.configure('TNotebook', background='#f0f8ff')
        style.configure('TNotebook.Tab', padding=[10, 5])

        style.configure("Social.TFrame", background="#c4ffc8")
        style.configure("Emotional.TFrame", background="#ffdbf4")
        style.configure("Productivity.TFrame", background="#dbecff")
        style.configure("Mindful.TFrame", background="#fffbdb")
        style.configure("Breathing.TFrame", background="#decaf3")
        self.create_widgets()

    def create_widgets(self):
        # Notebook for different sections
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Social Preparation Frame
        self.social_frame = ttk.Frame(self.notebook,style="Social.TFrame")
        self.notebook.add(self.social_frame, text="Social Preparation")
        self.create_social_prep_tab()

        # Emotional Control Frame
        self.emotion_frame = ttk.Frame(self.notebook, style="Emotional.TFrame")
        self.notebook.add(self.emotion_frame, text="Emotional Control")
        self.create_emotion_tab()

        # Productivity Frame
        self.productivity_frame = ttk.Frame(self.notebook, style="Productivity.TFrame")
        self.notebook.add(self.productivity_frame, text="Productivity Boost")
        self.create_productivity_tab()

        # Journal Frame
        self.journal_frame = ttk.Frame(self.notebook,style="Mindful.TFrame")
        self.notebook.add(self.journal_frame, text="Mindful Journal")
        self.create_journal_tab()

        # Breathing Exercise Frame
        self.breathing_frame = ttk.Frame(self.notebook,style="Breathing.TFrame")
        self.notebook.add(self.breathing_frame, text="Breathing Exercise")
        self.create_breathing_tab()

    def create_social_prep_tab(self):
        # Social Preparation Content
        title_label = ttk.Label(self.social_frame,
                                text="Social Situation Preparation",
                                font=('Helvetica', 14, 'bold'),
                                background="#c4ffc8")
        title_label.pack(pady=10)

        self.social_context = ttk.Combobox(self.social_frame,
                                           values=["Job Interview", "Networking Event",
                                                   "First Date", "Public Speaking",
                                                   "Meeting New People", "Social Gathering"])
        self.social_context.set("Select a social situation")
        self.social_context.pack(pady=5, padx=20, fill='x')

        generate_btn = ttk.Button(self.social_frame, text="Get Tips",
                                  command=self.generate_social_tips)
        generate_btn.pack(pady=10)

        self.social_tips = tk.Text(self.social_frame, height=15, wrap='word',
                                   bg='white', padx=10, pady=10,font=('Helvetica', 11, 'bold'))
        self.social_tips.pack(pady=10, padx=10, fill='both', expand=True)

        # Pre-populate with general tips
        self.social_tips.insert('end', "Select a social situation above and click 'Get Tips' for personalized advice.")

    def generate_social_tips(self):
        context = self.social_context.get()
        if context == "Select a social situation":
            messagebox.showwarning("Warning", "Please select a social situation first.")
            return

        tips = {
            "Job Interview": [
                "1. Research the company thoroughly - knowledge reduces anxiety",
                "2. Prepare answers to common questions but don't memorize them",
                "3. Practice power poses before the interview",
                "4. Arrive 15 minutes early to acclimate to the environment",
                "5. Remember: they want you to succeed - they invited you!",
                "6. Prepare 2-3 thoughtful questions to ask at the end",
                "7. Focus on your breathing if you feel nervous",
                "8. Dress comfortably professional to feel confident",
                "9. Bring water - it gives you natural pauses",
                "10. Remember past successes to boost confidence"
            ],
            "Networking Event": [
                "1. Set a realistic goal (e.g., talk to 3 new people)",
                "2. Prepare a 30-second introduction about yourself",
                "3. Identify open body language (people standing alone or in open groups)",
                "4. Bring business cards to feel prepared",
                "5. Ask open-ended questions - people love to talk about themselves",
                "6. Have an exit phrase ready ('Excuse me, I need to grab a drink')",
                "7. Remember most people feel some social anxiety",
                "8. Take breaks in the bathroom if overwhelmed",
                "9. Follow up with 2-3 people afterward via email/LinkedIn",
                "10. Reward yourself afterward for stepping out of comfort zone"
            ],
            "First Date": [
                "1. Choose a comfortable, public location",
                "2. Plan some conversation topics but stay flexible",
                "3. Remember it's about mutual fit, not impressing them",
                "4. Focus on being genuinely interested rather than interesting",
                "5. Practice self-compassion - dating is challenging for everyone",
                "6. Have a backup plan if you need to leave early",
                "7. Remind yourself they're probably nervous too",
                "8. Avoid alcohol if you're anxious - it can amplify emotions",
                "9. Wear something that makes you feel confident",
                "10. Breathe deeply before entering the venue"
            ],
            "Public Speaking": [
                "1. Practice multiple times, but don't aim for perfection",
                "2. Visit the venue beforehand if possible",
                "3. Focus on helping the audience rather than being judged",
                "4. Prepare notes with key points in large font",
                "5. Remember the audience wants you to succeed",
                "6. Practice grounding techniques before starting",
                "7. Have water available for natural pauses",
                "8. Move your body before speaking to release tension",
                "9. Visualize success the night before",
                "10. Accept that some nervousness is normal and even helpful"
            ],
            "Meeting New People": [
                "1. Arrive early to acclimate to the environment",
                "2. Prepare some open-ended questions in advance",
                "3. Focus on listening rather than worrying about what to say",
                "4. Remember names by repeating them immediately",
                "5. Find common ground - shared experiences build connection",
                "6. Take breaks if needed - bathroom visits are acceptable",
                "7. Smile and make eye contact (but don't stare)",
                "8. Have an exit strategy if you feel overwhelmed",
                "9. Remind yourself most people are focused on themselves",
                "10. Celebrate small victories in socializing"
            ],
            "Social Gathering": [
                "1. Set realistic expectations - you don't need to talk to everyone",
                "2. Identify a 'safe person' you can return to if anxious",
                "3. Prepare some recent stories or topics to discuss",
                "4. Have a drink in hand (non-alcoholic is fine) to feel less awkward",
                "5. Take listening breaks where you just observe",
                "6. Practice grounding techniques if feeling overwhelmed",
                "7. Set a time limit for yourself if needed",
                "8. Wear comfortable clothing to feel at ease",
                "9. Remember that leaving early is okay",
                "10. Reflect afterward on what went well"
            ]
        }

        self.social_tips.delete(1.0, 'end')
        self.social_tips.insert('end', f"Preparation Tips for {context}:\n\n")
        for tip in tips[context]:
            self.social_tips.insert('end', tip + "\n\n")

    def create_emotion_tab(self):
        # Emotional Control Content
        title_label = ttk.Label(self.emotion_frame,
                                text="Emotional Intelligence & Regulation",
                                font=('Helvetica', 14, 'bold'),
                                background="#ffdbf4")
        title_label.pack(pady=10)

        self.emotion_context = ttk.Combobox(self.emotion_frame,
                                            values=["Feeling Overwhelmed", "Anger/Frustration",
                                                    "Anxiety", "Sadness", "Conflict Situation",
                                                    "Need to Make Important Decision"])
        self.emotion_context.set("Select emotional state")
        self.emotion_context.pack(pady=5, padx=20, fill='x')

        generate_btn = ttk.Button(self.emotion_frame, text="Get Strategies",
                                  command=self.generate_emotion_tips)
        generate_btn.pack(pady=10)

        self.emotion_tips = tk.Text(self.emotion_frame, height=15, wrap='word',
                                    bg='white', padx=10, pady=10,font=('Helvetica', 11, 'bold'))
        self.emotion_tips.pack(pady=10, padx=10, fill='both', expand=True)

        # Pre-populate with general tips
        self.emotion_tips.insert('end',
                                 "Select an emotional state above and click 'Get Strategies' for regulation techniques.")

    def generate_emotion_tips(self):
        context = self.emotion_context.get()
        if context == "Select emotional state":
            messagebox.showwarning("Warning", "Please select an emotional state first.")
            return

        tips = {
            "Feeling Overwhelmed": [
                "1. Practice the 5-4-3-2-1 grounding technique",
                "2. Break tasks into tiny, manageable steps",
                "3. Give yourself permission to pause and breathe",
                "4. Drink water - dehydration amplifies stress",
                "5. Create physical space (step outside if possible)",
                "6. Use positive self-talk ('I can handle this step by step')",
                "7. Prioritize - what absolutely must be done now?",
                "8. Set a timer for 5 minutes of focused work",
                "9. Acknowledge your feelings without judgment",
                "10. Remember this is temporary - emotions are waves that pass"
            ],
            "Anger/Frustration": [
                "1. Take 5 deep breaths before responding",
                "2. Remove yourself from the situation temporarily",
                "3. Identify the underlying need not being met",
                "4. Use 'I feel' statements rather than accusations",
                "5. Channel energy physically (walk, squeeze a stress ball)",
                "6. Write down your thoughts before speaking",
                "7. Consider the other perspective with curiosity",
                "8. Ask for a timeout if needed ('I need a moment')",
                "9. Remind yourself that anger is a signal, not a solution",
                "10. Practice radical acceptance of what you can't change"
            ],
            "Anxiety": [
                "1. Practice box breathing (4-4-4-4 count)",
                "2. Challenge catastrophic thoughts with evidence",
                "3. Focus on your senses (name 5 things you see, etc.)",
                "4. Remind yourself anxiety is a false alarm system",
                "5. Use progressive muscle relaxation",
                "6. Limit caffeine and sugar which amplify anxiety",
                "7. Create a 'worry period' later in the day",
                "8. Practice self-compassion - anxiety is common",
                "9. Focus on the present moment (not future what-ifs)",
                "10. Remember past times you've handled anxiety successfully"
            ],
            "Sadness": [
                "1. Allow yourself to feel without judgment",
                "2. Connect with supportive people, even briefly",
                "3. Engage in small acts of self-care",
                "4. Get sunlight and fresh air if possible",
                "5. Express feelings through writing or art",
                "6. Recall past challenges you've overcome",
                "7. Avoid isolation, even if you don't feel like socializing",
                "8. Practice gratitude for small things",
                "9. Consider professional help if prolonged",
                "10. Remember emotions are temporary states, not permanent"
            ],
            "Conflict Situation": [
                "1. Listen actively before formulating your response",
                "2. Use 'I' statements to express your perspective",
                "3. Look for common ground and shared goals",
                "4. Take breaks if emotions escalate",
                "5. Focus on the issue, not personal attacks",
                "6. Consider what part you may have played",
                "7. Aim for understanding rather than winning",
                "8. Be willing to compromise where possible",
                "9. Separate the person from the problem",
                "10. Know when to disengage if unproductive"
            ],
            "Need to Make Important Decision": [
                "1. List pros and cons clearly on paper",
                "2. Consider your values - what aligns best?",
                "3. Imagine advising a friend in this situation",
                "4. Sleep on it - decisions often clearer after rest",
                "5. Identify worst-case scenarios - are they manageable?",
                "6. Consult trusted advisors for perspective",
                "7. Avoid deciding when emotionally charged",
                "8. Consider the 10-10-10 rule (impact in 10 days/months/years)",
                "9. Trust your intuition after gathering facts",
                "10. Remember most decisions aren't irreversible"
            ]
        }

        self.emotion_tips.delete(1.0, 'end')
        self.emotion_tips.insert('end', f"Emotional Regulation Strategies for {context}:\n\n")
        for tip in tips[context]:
            self.emotion_tips.insert('end', tip + "\n\n")

    def create_productivity_tab(self):
        # Productivity Content
        title_label = ttk.Label(self.productivity_frame,
                                text="Productivity When You're Not at Your Best",
                                font=('Helvetica', 14, 'bold'),
                                background="#dbecff")
        title_label.pack(pady=10)

        self.energy_level = ttk.Combobox(self.productivity_frame,
                                         values=["Extremely Low Energy", "Moderately Low",
                                                 "Brain Fog", "Emotionally Drained",
                                                 "Physically Tired", "Mild Depression"])
        self.energy_level.set("Select your energy state")
        self.energy_level.pack(pady=5, padx=20, fill='x')

        generate_btn = ttk.Button(self.productivity_frame, text="Get Productivity Tips",
                                  command=self.generate_productivity_tips)
        generate_btn.pack(pady=10)

        self.productivity_tips = tk.Text(self.productivity_frame, height=15, wrap='word',
                                         bg='white', padx=10, pady=10,font=('Helvetica', 11, 'bold'))
        self.productivity_tips.pack(pady=10, padx=10, fill='both', expand=True)

        # Pre-populate with general tips
        self.productivity_tips.insert('end', "Select your energy state above for tailored productivity strategies.")

    def generate_productivity_tips(self):
        context = self.energy_level.get()
        if context == "Select your energy state":
            messagebox.showwarning("Warning", "Please select your energy state first.")
            return

        tips = {
            "Extremely Low Energy": [
                "1. Accept where you're at - fighting it wastes energy",
                "2. Do just one tiny task to build momentum",
                "3. Use the 5-minute rule (commit to just 5 minutes)",
                "4. Focus on self-care first (hydration, snack, stretch)",
                "5. Break tasks into absurdly small steps",
                "6. Alternate between rest and micro-work sessions",
                "7. Prioritize - what absolutely must be done today?",
                "8. Use body doubling (work alongside someone)",
                "9. Lower expectations - something is better than nothing",
                "10. Celebrate any small accomplishment"
            ],
            "Moderately Low": [
                "1. Use the Pomodoro technique (25/5)",
                "2. Start with easiest tasks to build momentum",
                "3. Create a 'done list' to track progress",
                "4. Eliminate distractions (phone in another room)",
                "5. Work in a different environment if possible",
                "6. Use upbeat music without lyrics",
                "7. Set a timer for focused work bursts",
                "8. Reward yourself after milestones",
                "9. Stay hydrated - dehydration causes fatigue",
                "10. Move your body periodically"
            ],
            "Brain Fog": [
                "1. Do a brain dump of all thoughts first",
                "2. Work in very short bursts with breaks",
                "3. Use simple, concrete tasks",
                "4. Try changing your physical position",
                "5. Chew gum or suck on mints for focus",
                "6. Reduce sensory input (noise-canceling headphones)",
                "7. Use external tools (lists, timers, reminders)",
                "8. Avoid multitasking - single-tasking only",
                "9. Try a short walk or stretching",
                "10. Accept this state - forcing may worsen fog"
            ],
            "Emotionally Drained": [
                "1. Acknowledge your emotional state first",
                "2. Set very modest goals for the day",
                "3. Use grounding techniques between tasks",
                "4. Alternate work with self-care moments",
                "5. Focus on mechanical tasks if possible",
                "6. Use compassionate self-talk",
                "7. Connect briefly with supportive people",
                "8. Avoid emotionally demanding tasks if possible",
                "9. Practice micro-productivity (small wins)",
                "10. Remember this is temporary"
            ],
            "Physically Tired": [
                "1. Take a 20-minute power nap if possible",
                "2. Hydrate and have a protein snack",
                "3. Work in a brightly lit area",
                "4. Alternate sitting and standing",
                "5. Do light stretches every 30 minutes",
                "6. Prioritize tasks requiring less mental effort",
                "7. Use caffeine strategically (if it works for you)",
                "8. Break work into small chunks with movement breaks",
                "9. Listen to upbeat music",
                "10. Consider if rest might be more productive long-term"
            ],
            "Mild Depression": [
                "1. Set one small, achievable goal",
                "2. Use behavioral activation - action before motivation",
                "3. Create structure with time blocking",
                "4. Focus on completion, not perfection",
                "5. Get sunlight exposure early in the day",
                "6. Move your body, even just walking",
                "7. Connect with others, even briefly",
                "8. Celebrate tiny accomplishments",
                "9. Avoid isolation - work in a cafe or with others",
                "10. Remember this state doesn't define you"
            ]
        }

        self.productivity_tips.delete(1.0, 'end')
        self.productivity_tips.insert('end', f"Productivity Strategies for {context}:\n\n")
        for tip in tips[context]:
            self.productivity_tips.insert('end', tip + "\n\n")

    def create_journal_tab(self):
        # Journaling Content
        title_label = ttk.Label(self.journal_frame,
                                text="Mindful Journaling",
                                font=('Helvetica', 14, 'bold'),
                                background="#fffbdb")
        title_label.pack(pady=10)

        prompt_label = ttk.Label(self.journal_frame,
                                 text="Journal Prompt:",
                                 font=('Helvetica', 11),
                                 background="#fffbdb")
        prompt_label.pack(pady=5)

        self.prompt_text = tk.Text(self.journal_frame, height=3, wrap='word',
                                   bg='white', padx=10, pady=10,font=('Helvetica', 11, 'bold'))
        self.prompt_text.pack(pady=5, padx=10, fill='x')

        new_prompt_btn = ttk.Button(self.journal_frame, text="New Prompt",
                                    command=self.generate_journal_prompt)
        new_prompt_btn.pack(pady=5)

        self.journal_entry = tk.Text(self.journal_frame, height=15, wrap='word',
                                     bg='white', padx=10, pady=10,font=('Helvetica', 11, 'bold'))
        self.journal_entry.pack(pady=10, padx=10, fill='both', expand=True)

        save_btn = ttk.Button(self.journal_frame, text="Save Entry",
                              command=self.save_journal_entry)
        save_btn.pack(pady=5)

        # Generate first prompt
        self.generate_journal_prompt()

    def generate_journal_prompt(self):
        prompts = [
            "What emotions am I feeling right now? Where do I feel them in my body?",
            "What's one small win I've had recently, no matter how small?",
            "What thought patterns have been repeating in my mind lately?",
            "If my best friend was feeling this way, what would I tell them?",
            "What's one thing I'm grateful for today, and why?",
            "What would my ideal day look like? What small piece can I incorporate today?",
            "What's something I've been avoiding that might help me feel better?",
            "How have I grown or changed in the past year?",
            "What boundaries do I need to set or reinforce?",
            "What's a self-care practice I've been neglecting that I could revisit?",
            "What negative thought keeps coming up? How can I reframe it?",
            "What's one small step I can take today toward a goal that matters to me?",
            "What relationships energize me? Which ones drain me?",
            "What did I love doing as a child that I might enjoy now?",
            "What's something I need to forgive myself for?",
            "What does my inner critic say? How would my inner coach respond?",
            "What's a recent challenge and what did I learn from it?",
            "What values are most important to me? Am I living in alignment?",
            "What's one thing I can let go of that no longer serves me?",
            "How would I describe my current season of life in 3 words?"
        ]

        prompt = random.choice(prompts)
        self.prompt_text.delete(1.0, 'end')
        self.prompt_text.insert('end', prompt)

    def save_journal_entry(self):
        entry = self.journal_entry.get(1.0, 'end-1c')
        prompt = self.prompt_text.get(1.0, 'end-1c')

        if not entry.strip():
            messagebox.showwarning("Warning", "Journal entry is empty!")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        filename = f"journal_{datetime.now().strftime('%Y%m%d')}.txt"

        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"\n\n--- Entry from {timestamp} ---\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(entry)

            messagebox.showinfo("Success", f"Journal entry saved to {filename}")
            self.journal_entry.delete(1.0, 'end')
            self.generate_journal_prompt()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save journal: {str(e)}")

    def create_breathing_tab(self):
        # Breathing Exercise Content
        title_label = ttk.Label(self.breathing_frame,
                                text="Guided Breathing Exercise",
                                font=('Helvetica', 14, 'bold'),
                                background="#decaf3")
        title_label.pack(pady=10)

        self.breath_pattern = ttk.Combobox(self.breathing_frame,
                                           values=["Calming (4-7-8)",
                                                   "Energy Boost (Box Breathing)",
                                                   "Anxiety Relief (Equal Breathing)",
                                                   "Stress Reduction (4-4-6-2)"])
        self.breath_pattern.set("Select breathing pattern")
        self.breath_pattern.pack(pady=5, padx=20, fill='x')

        self.breath_canvas = tk.Canvas(self.breathing_frame, width=300, height=300,
                                       bg='white', highlightthickness=0)
        self.breath_canvas.pack(pady=20)

        self.breath_label = ttk.Label(self.breathing_frame,
                                      text="Select a breathing pattern to begin",
                                      font=('Helvetica', 12, 'bold'),
                                      background="#decaf3")
        self.breath_label.pack(pady=5)

        start_btn = ttk.Button(self.breathing_frame, text="Start Exercise",
                               command=self.start_breathing_exercise)
        start_btn.pack(pady=10)

        self.breath_cycle = 0
        self.breath_phase = "inhale"
        self.breath_timer = None
        self.breath_remaining = 0

    def start_breathing_exercise(self):
        pattern = self.breath_pattern.get()
        if pattern == "Select breathing pattern":
            messagebox.showwarning("Warning", "Please select a breathing pattern first.")
            return

        if self.breath_timer:
            self.root.after_cancel(self.breath_timer)

        self.breath_cycle = 0
        self.breath_phase = "inhale"

        if pattern == "Calming (4-7-8)":
            self.breath_timings = {"inhale": 4, "hold": 7, "exhale": 8}
            self.breath_steps = ["inhale", "hold", "exhale"]
        elif pattern == "Energy Boost (Box Breathing)":
            self.breath_timings = {"inhale": 4, "hold": 4, "exhale": 4, "hold2": 4}
            self.breath_steps = ["inhale", "hold", "exhale", "hold2"]
        elif pattern == "Anxiety Relief (Equal Breathing)":
            self.breath_timings = {"inhale": 4, "exhale": 4}
            self.breath_steps = ["inhale", "exhale"]
        elif pattern == "Stress Reduction (4-4-6-2)":
            self.breath_timings = {"inhale": 4, "hold": 4, "exhale": 6, "hold2": 2}
            self.breath_steps = ["inhale", "hold", "exhale", "hold2"]

        self.breath_remaining = self.breath_timings[self.breath_phase]
        self.update_breathing_display()
        self.run_breathing_cycle()

    def run_breathing_cycle(self):
        if self.breath_remaining > 0:
            self.breath_remaining -= 1
            self.update_breathing_display()
            self.breath_timer = self.root.after(1000, self.run_breathing_cycle)
        else:
            next_index = (self.breath_steps.index(self.breath_phase) + 1) % len(self.breath_steps)
            self.breath_phase = self.breath_steps[next_index]

            if self.breath_phase == "inhale" and next_index == 0:
                self.breath_cycle += 1
                if self.breath_cycle >= 5:  # Complete 5 cycles
                    self.breath_label.config(text="Exercise complete! Feel free to start again.")
                    return

            self.breath_remaining = self.breath_timings[self.breath_phase]
            self.update_breathing_display()
            self.breath_timer = self.root.after(1000, self.run_breathing_cycle)

    def update_breathing_display(self):
        self.breath_canvas.delete("all")

        # Draw circle that changes size and color based on phase
        if self.breath_phase == "inhale":
            color = "green"
            radius = 50 + (self.breath_timings["inhale"] - self.breath_remaining) * 20
        elif self.breath_phase == "exhale":
            color = "blue"
            radius = 150 - (self.breath_timings["exhale"] - self.breath_remaining) * 20
        else:  # hold phases
            color = "yellow"
            radius = 150

        x, y = 150, 150
        self.breath_canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                       fill=color, outline="")

        # Display instructions
        phase_text = {
            "inhale": "Breathe In",
            "exhale": "Breathe Out",
            "hold": "Hold",
            "hold2": "Pause"
        }

        self.breath_label.config(
            text=f"{phase_text[self.breath_phase]} ({self.breath_remaining}s)\n"
                 f"Cycle: {self.breath_cycle + 1}/5\n"
                 f"Pattern: {self.breath_pattern.get()}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MentalHealthApp(root)
    root.mainloop()
