from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from groq import Groq

class TextProcessView(APIView):
    def post(self, request):
        input_text = request.data.get('text')
        
        # Check if input_text is provided
        if not input_text:
            return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Initialize the Groq client
        client = Groq(api_key='GROQ_API_KEY')
        
        # Convert user input to prompt with additional context and examples
        prompt = (
            "You are a helpful assistant. "
            "create a well-defined prompt to get the best results on this topic. "
            "Make sure the prompt is clear, concise, and includes relevant details. "
            "Make sure if any  coding is related you just give prompt to genreate entire code from scratch to end with directory structure"
            "For example, if the input is about AI, the prompt should focus on AI-related queries. "
            "Input text: '{input_text}'"
        ).format(input_text=input_text)
        
        try:
            # Get the LLM response
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "you are a helpful assistant. Answer as Jon Snow"
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-70b-8192",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )
            
            crafted_prompt = chat_completion.choices[0].message.content
            return Response({'crafted_prompt': crafted_prompt}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
