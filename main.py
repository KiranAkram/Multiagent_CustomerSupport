import streamlit as st
from crewai import Crew
from agents import support_agent, support_quality_assurance_agent
from tasks import get_inquiry_resolution_task, quality_assurance_review
import nest_asyncio
import logging
import os


os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

# Set the logging level for httpx to WARNING to suppress INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)

nest_asyncio.apply()


def main():
    # Streamlit UI
    st.title("Customer Support Multi-Agent System")
    st.write("Provide the following detailss to generate a support response:")

    # Input fields
    customer = st.text_input("your organization name", value="")
    person = st.text_input("Person name", value="")
    customercare_company = st.text_input("customer care company name", value="")
    inquiry = st.text_area(
        "Inquiry",
        value="",
    )
    website = st.text_input("Website", value="")

    # Button to trigger the multi-agent system
    if st.button("Get Support Response"):
        inputs = {
            "customer": customer,
            "person": person,
            "inquiry": inquiry,
            "website": website,
            "customercare_company": customercare_company,
        }
        # Dynamically create the inquiry resolution task with the provided website URL
        inquiry_resolution = get_inquiry_resolution_task(website_url=inputs["website"])

        # Create crew with the dynamic inquiry resolution task
        crew = Crew(
            agents=[support_agent, support_quality_assurance_agent],
            tasks=[inquiry_resolution, quality_assurance_review],
            verbose=0,
            memory=True,
        )

        result = crew.kickoff(inputs=inputs)

        # Display result as markdown
        st.markdown(f"### Response:\n{result}")


if __name__ == "__main__":
    main()
