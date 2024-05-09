import streamlit as st
from openai import OpenAI


# Título da página
st.title('Features de Anúncios de Produtos')

# APIKEY
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Definir o modelo do GPT
if "openai_model" not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# Definir a mensagem inicial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'assistant',
         'content': """Olá! Esse assistente serve para gerar features a partir de um título e descrição de um anúncio
                    de produto da web.
                    Bastar inputar algum texto com essas informações."""
         }]

# Exibir a mensagem inicial
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


# Criação do campo de input
def process_input(prompt, client):
    if prompt:
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)

        with (st.chat_message('assistant')):
            message_placeholder = st.empty()
            message_placeholder.markdown('gerando resposta...')

            st.session_state['question_sent'] = True

            # Criação do chat completions e parametrização do perfil do assistente
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system',
                     'content': """Você deve receber duas informações (título e descrição), entender o conteúdo e 
                                gerar um json com as features.
                                Os dados são de anúncios de produtos online.

                                Exemplo de entrada:
                                'Título: FYY Leather Case with Mirror for Samsung Galaxy S8 Plus, 
                                Leather Wallet Flip Folio Case with Mirror and Wrist Strap for Samsung Galaxy S8 Plus 
                                Black

                                Descrição do Produto: 
                                Premium PU Leather Top quality. Made with Premium PU Leather. 
                                Receiver design. Accurate cut-out for receiver. Convenient to Answer the phone without 
                                open the case. Hand strap makes it easy to carry around. RFID Technique: Radio Frequency 
                                Identification technology, through radio signals to identify specific targets and to 
                                read and copy electronic data. Most Credit Cards, Debit Cards, ID Cards are set-in the 
                                RFID chip, the RFID reader can easily read the cards information within 
                                10 feet(about 3m) without touching them. This case is designed to protect your cards 
                                information from stealing with blocking material of RFID shielding technology. 100% 
                                Handmade. Perfect craftsmanship and reinforced stitching make it even more durable. 
                                Sleek, practical, and elegant with a variety of dashing colors. Multiple Functions Card 
                                slots are designed for you to put your photo, debit card, credit card, or ID card while 
                                on the go. Unique design. Cosmetic Mirror inside made for your makeup and beauty. 
                                Perfect Viewing Angle. Kickstand function is convenient for movie-watching or 
                                video-chatting. Space amplification, convenient to unlock. Kickstand function is 
                                convenient for movie-watching or video-chatting.

                                Exemplo de saída:
                                Features: {
                                  "category": "Phone Accessories",                                        
                                  "material": "Premium PU Leather",                                        
                                  "features": {                                        
                                    "receiver_design": "Accurate cut-out for receiver. Convenient to Answer the phone 
                                    without opening the case.",
                                    "hand_strap": "Yes",                                
                                    "RFID_technique": "Protection of card information with RFID shielding technology",                                
                                    "handmade": "100% Handmade",                                
                                    "stitching": "Reinforced stitching",                                
                                    "functions": {                                
                                      "card_slots": "Yes",                                
                                      "cosmetic_mirror": "Yes",                               
                                      "kickstand_function": "Yes, convenient for movie-watching or video-chatting",                                
                                      "space_amplification": "Yes, convenient to unlock"                                
                                    },                                
                                    "color_options": "Variety of dashing colors",                                
                                    "compatibility": "Samsung Galaxy S8 Plus"                                
                                  }                                        
                                }
                                você deve retornar sempre formatado e identado como JSON"""},
                    {'role': 'user', 'content': prompt}
                ],
                stream=True  # habilita a exibição da resposta por 'partes'
            )

            # Exibição da resposta em stream
            full_response = ''
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response)

            st.session_state.messages.append({'role': 'assistant', 'content': full_response})


# Criação do campo de input
if prompt := st.chat_input('Digite o título e descrição do produto aqui:'):
    process_input(prompt, client)
