import streamlit as st
import json
import datetime
import time
from groq import Groq
import base64
from io import BytesIO
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="GPT Web App - Powered by Groq",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .assistant-message {
        background-color: #28a745;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .sidebar-header {
        color: #1f77b4;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {"Default": []}
    if "current_session" not in st.session_state:
        st.session_state.current_session = "Default"
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = "You are a helpful AI assistant."
    if "model_settings" not in st.session_state:
        st.session_state.model_settings = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9
        }

initialize_session_state()

# Sidebar configuration
with st.sidebar:
    st.markdown('<p class="sidebar-header">🛠️ Configuration</p>', unsafe_allow_html=True)
    
    # API Key
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        value="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",
        help="Enter your Groq API key"
    )
    
    # Model selection
    model_options = [
        "llama-3.3-70b-versatile",
        "llama3-8b-8192",
        "llama3-70b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it",
        "gemma2-9b-it"
    ]
    
    selected_model = st.selectbox(
        "🤖 Select Model",
        model_options,
        index=0
    )
    
    # Model parameters
    st.markdown("### 🎛️ Model Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, st.session_state.model_settings["temperature"], 0.1)
    max_tokens = st.slider("Max Tokens", 100, 4000, st.session_state.model_settings["max_tokens"], 100)
    top_p = st.slider("Top P", 0.0, 1.0, st.session_state.model_settings["top_p"], 0.1)
    
    # Update model settings
    st.session_state.model_settings = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p
    }
    
    # System prompt
    st.markdown("### 🎭 System Prompt")
    system_prompt = st.text_area(
        "System Prompt",
        value=st.session_state.system_prompt,
        height=100,
        help="Define the AI's behavior and personality"
    )
    st.session_state.system_prompt = system_prompt
    
    # Chat sessions management
    st.markdown("### 💬 Chat Sessions")
    
    # Create new session
    new_session_name = st.text_input("New Session Name")
    if st.button("➕ Create Session") and new_session_name:
        if new_session_name not in st.session_state.chat_sessions:
            st.session_state.chat_sessions[new_session_name] = []
            st.session_state.current_session = new_session_name
            st.success(f"Created session: {new_session_name}")
            st.rerun()
    
    # Select session
    current_session = st.selectbox(
        "Select Session",
        list(st.session_state.chat_sessions.keys()),
        index=list(st.session_state.chat_sessions.keys()).index(st.session_state.current_session)
    )
    
    if current_session != st.session_state.current_session:
        st.session_state.current_session = current_session
        st.session_state.messages = st.session_state.chat_sessions[current_session].copy()
        st.rerun()
    
    # Delete session
    if st.button("🗑️ Delete Current Session") and len(st.session_state.chat_sessions) > 1:
        del st.session_state.chat_sessions[st.session_state.current_session]
        st.session_state.current_session = list(st.session_state.chat_sessions.keys())[0]
        st.session_state.messages = st.session_state.chat_sessions[st.session_state.current_session].copy()
        st.success("Session deleted!")
        st.rerun()
    
    # Export/Import
    st.markdown("### 📁 Data Management")
    
    # Export conversations
    if st.button("📤 Export Conversations"):
        export_data = {
            "sessions": st.session_state.chat_sessions,
            "export_date": datetime.datetime.now().isoformat(),
            "model_settings": st.session_state.model_settings,
            "system_prompt": st.session_state.system_prompt
        }
        
        json_str = json.dumps(export_data, indent=2)
        b64 = base64.b64encode(json_str.encode()).decode()
        
        st.download_button(
            label="💾 Download Conversations",
            data=json_str,
            file_name=f"gpt_conversations_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Import conversations
    uploaded_file = st.file_uploader("📥 Import Conversations", type=['json'])
    if uploaded_file is not None:
        try:
            import_data = json.load(uploaded_file)
            st.session_state.chat_sessions.update(import_data.get("sessions", {}))
            if "model_settings" in import_data:
                st.session_state.model_settings.update(import_data["model_settings"])
            if "system_prompt" in import_data:
                st.session_state.system_prompt = import_data["system_prompt"]
            st.success("Conversations imported successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error importing file: {str(e)}")
    
    # Clear current conversation
    if st.button("🧹 Clear Current Conversation"):
        st.session_state.messages = []
        st.session_state.chat_sessions[st.session_state.current_session] = []
        st.rerun()

# Main content area
st.markdown('<h1 class="main-header">🤖 GPT Web App - Powered by Groq</h1>', unsafe_allow_html=True)

# Tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "📊 Analytics", "🎨 Prompt Templates", "📚 Knowledge Base", "⚙️ Advanced"])

with tab1:
    # Chat interface
    st.markdown("### 💬 AI Chat Assistant")
    
    # Display current session info
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info(f"Current Session: **{st.session_state.current_session}**")
    with col2:
        st.metric("Messages", len(st.session_state.messages))
    with col3:
        st.metric("Model", selected_model.split('-')[0].upper())
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(f"🕒 {message['timestamp']}")
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not groq_api_key:
            st.error("⚠️ Please enter your Groq API key in the sidebar!")
        else:
            # Add user message
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_message = {"role": "user", "content": prompt, "timestamp": timestamp}
            st.session_state.messages.append(user_message)
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
                st.caption(f"🕒 {timestamp}")
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    try:
                        client = Groq(api_key=groq_api_key)
                        
                        # Prepare messages for API
                        messages = [{"role": "system", "content": st.session_state.system_prompt}]
                        messages.extend([{"role": msg["role"], "content": msg["content"]} 
                                       for msg in st.session_state.messages])
                        
                        # Generate response
                        response = client.chat.completions.create(
                            model=selected_model,
                            messages=messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                            stream=True
                        )
                        
                        # Stream response
                        response_placeholder = st.empty()
                        full_response = ""
                        
                        for chunk in response:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                response_placeholder.markdown(full_response + "▌")
                        
                        response_placeholder.markdown(full_response)
                        
                        # Add assistant message
                        assistant_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        assistant_message = {
                            "role": "assistant", 
                            "content": full_response, 
                            "timestamp": assistant_timestamp
                        }
                        st.session_state.messages.append(assistant_message)
                        st.caption(f"🕒 {assistant_timestamp}")
                        
                        # Update session
                        st.session_state.chat_sessions[st.session_state.current_session] = st.session_state.messages.copy()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

with tab2:
    # Analytics dashboard
    st.markdown("### 📊 Conversation Analytics")
    
    if st.session_state.messages:
        # Message statistics
        total_messages = len(st.session_state.messages)
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("User Messages", user_messages)
        with col3:
            st.metric("AI Responses", assistant_messages)
        with col4:
            if user_messages > 0:
                avg_length = sum(len(m["content"]) for m in st.session_state.messages if m["role"] == "user") / user_messages
                st.metric("Avg User Message Length", f"{avg_length:.0f}")
        
        # Word count analysis
        st.markdown("#### 📝 Word Analysis")
        all_text = " ".join([m["content"] for m in st.session_state.messages])
        word_count = len(all_text.split())
        char_count = len(all_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Words", word_count)
        with col2:
            st.metric("Total Characters", char_count)
        
        # Session comparison
        st.markdown("#### 📈 Session Comparison")
        session_data = []
        for session_name, messages in st.session_state.chat_sessions.items():
            session_data.append({
                "Session": session_name,
                "Messages": len(messages),
                "User Messages": len([m for m in messages if m["role"] == "user"]),
                "AI Responses": len([m for m in messages if m["role"] == "assistant"])
            })
        
        if session_data:
            df = pd.DataFrame(session_data)
            st.dataframe(df, use_container_width=True)
            
            # Charts
            col1, col2 = st.columns(2)
            with col1:
                st.bar_chart(df.set_index("Session")["Messages"])
            with col2:
                st.line_chart(df.set_index("Session")[["User Messages", "AI Responses"]])
    else:
        st.info("Start a conversation to see analytics!")

with tab3:
    # Prompt templates
    st.markdown("### 🎨 Prompt Templates")
    
    # Predefined templates
    templates = {
        "Creative Writing": "You are a creative writing assistant. Help me write engaging stories, poems, or creative content. Be imaginative and inspiring.",
        "Code Assistant": "You are an expert programmer. Help me write, debug, and optimize code. Provide clear explanations and best practices.",
        "Academic Tutor": "You are a knowledgeable academic tutor. Explain complex topics clearly, provide examples, and help with learning.",
        "Business Advisor": "You are a business consultant. Provide strategic advice, market insights, and business solutions.",
        "Language Teacher": "You are a language teacher. Help me learn new languages, correct my grammar, and practice conversations.",
        "Research Assistant": "You are a research assistant. Help me find information, analyze data, and provide well-researched answers.",
        "Therapist": "You are a supportive therapist. Listen empathetically and provide thoughtful, caring responses.",
        "Chef": "You are a professional chef. Help me with recipes, cooking techniques, and culinary advice."
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### 📝 Quick Templates")
        for name, template in templates.items():
            if st.button(f"🎯 {name}", key=f"template_{name}"):
                st.session_state.system_prompt = template
                st.success(f"Applied {name} template!")
                st.rerun()
    
    with col2:
        st.markdown("#### ✏️ Custom Template")
        custom_template = st.text_area(
            "Create Your Own Template",
            height=200,
            placeholder="Write your custom system prompt here..."
        )
        
        if st.button("💾 Save Custom Template"):
            st.session_state.system_prompt = custom_template
            st.success("Custom template applied!")
            st.rerun()
    
    # Template library
    st.markdown("#### 📚 Template Preview")
    selected_template = st.selectbox("Preview Template", list(templates.keys()))
    st.text_area("Template Content", templates[selected_template], height=100, disabled=True)

with tab4:
    # Knowledge base
    st.markdown("### 📚 Knowledge Base")
    
    st.markdown("#### 🔍 Quick References")
    
    # FAQ section
    with st.expander("❓ Frequently Asked Questions"):
        st.markdown("""
        **Q: How do I get better responses?**
        A: Be specific in your prompts, provide context, and use the system prompt to set the AI's behavior.
        
        **Q: Can I save my conversations?**
        A: Yes! Use the export function in the sidebar to download your conversations.
        
        **Q: Which model should I choose?**
        A: Llama-3.3-70B is great for general tasks, Mixtral for complex reasoning, and Gemma for lightweight tasks.
        
        **Q: What do the parameters do?**
        A: Temperature controls creativity (higher = more creative), Max Tokens limits response length, Top P affects word choice diversity.
        """)
    
    # Tips and tricks
    with st.expander("💡 Tips and Tricks"):
        st.markdown("""
        **🎯 Writing Better Prompts:**
        - Be specific and clear about what you want
        - Provide examples when possible
        - Break complex tasks into smaller steps
        - Use role-playing prompts for specialized knowledge
        
        **⚡ Optimizing Performance:**
        - Lower temperature (0.1-0.3) for factual responses
        - Higher temperature (0.7-1.0) for creative tasks
        - Adjust max tokens based on desired response length
        - Use system prompts to maintain consistent behavior
        
        **🔧 Advanced Techniques:**
        - Chain of thought: Ask the AI to think step by step
        - Few-shot learning: Provide examples in your prompt
        - Role specification: Define the AI's expertise area
        - Context setting: Provide relevant background information
        """)
    
    # Model comparison
    with st.expander("🤖 Model Comparison"):
        model_info = {
            "Model": ["Llama-3.3-70B", "Llama3-8B", "Llama3-70B", "Mixtral-8x7B", "Gemma-7B", "Gemma2-9B"],
            "Best For": ["General tasks", "Quick responses", "Complex reasoning", "Multi-domain", "Lightweight tasks", "Balanced performance"],
            "Speed": ["Medium", "Fast", "Slow", "Medium", "Very Fast", "Fast"],
            "Quality": ["Excellent", "Good", "Excellent", "Very Good", "Good", "Very Good"]
        }
        
        df = pd.DataFrame(model_info)
        st.dataframe(df, use_container_width=True)

with tab5:
    # Advanced features
    st.markdown("### ⚙️ Advanced Features")
    
    # Batch processing
    st.markdown("#### 🔄 Batch Processing")
    batch_prompts = st.text_area(
        "Enter multiple prompts (one per line)",
        height=150,
        placeholder="What is AI?\nHow does machine learning work?\nExplain neural networks."
    )
    
    if st.button("🚀 Process Batch") and batch_prompts and groq_api_key:
        prompts = [p.strip() for p in batch_prompts.split('\n') if p.strip()]
        
        with st.spinner(f"Processing {len(prompts)} prompts..."):
            client = Groq(api_key=groq_api_key)
            results = []
            
            progress_bar = st.progress(0)
            
            for i, prompt in enumerate(prompts):
                try:
                    messages = [
                        {"role": "system", "content": st.session_state.system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                    
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p
                    )
                    
                    results.append({
                        "Prompt": prompt,
                        "Response": response.choices[0].message.content
                    })
                    
                except Exception as e:
                    results.append({
                        "Prompt": prompt,
                        "Response": f"Error: {str(e)}"
                    })
                
                progress_bar.progress((i + 1) / len(prompts))
            
            # Display results
            st.markdown("#### 📋 Batch Results")
            for i, result in enumerate(results, 1):
                with st.expander(f"Result {i}: {result['Prompt'][:50]}..."):
                    st.markdown(f"**Prompt:** {result['Prompt']}")
                    st.markdown(f"**Response:** {result['Response']}")
            
            # Download results
            results_df = pd.DataFrame(results)
            csv = results_df.to_csv(index=False)
            st.download_button(
                "📥 Download Results (CSV)",
                csv,
                f"batch_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )
    
    # API usage statistics
    st.markdown("#### 📊 Session Statistics")
    if st.session_state.messages:
        total_tokens_estimate = sum(len(m["content"].split()) * 1.3 for m in st.session_state.messages)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Estimated Tokens Used", f"{total_tokens_estimate:.0f}")
        with col2:
            st.metric("Current Session Length", f"{len(st.session_state.messages)}")
        with col3:
            if st.session_state.messages:
                session_duration = "Active"
                st.metric("Session Status", session_duration)
    
    # System information
    st.markdown("#### ℹ️ System Information")
    system_info = {
        "Current Model": selected_model,
        "Temperature": temperature,
        "Max Tokens": max_tokens,
        "Top P": top_p,
        "Active Sessions": len(st.session_state.chat_sessions),
        "Current Session": st.session_state.current_session
    }
    
    for key, value in system_info.items():
        st.text(f"{key}: {value}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🤖 <strong>GPT Web App - Powered by Groq</strong></p>
        <p>Built with ❤️ using Streamlit • Advanced AI Chat Interface</p>
        <p>Features: Multi-session chat, Analytics, Templates, Batch processing, Export/Import</p>
    </div>
    """,
    unsafe_allow_html=True
)
