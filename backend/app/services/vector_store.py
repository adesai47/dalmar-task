import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import asyncio
import json
import os

class VectorStoreService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_model = None
        self.collection_name = "healthcare_docs"
        
    async def initialize(self):
        """Initialize ChromaDB client and embedding model"""
        try:
            # Initialize ChromaDB client
            self.client = chromadb.Client(Settings(
                persist_directory="./data/chroma_db",
                anonymized_telemetry=False
            ))
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create or get collection
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                print(f"Loaded existing collection: {self.collection_name}")
            except:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Healthcare documents collection"}
                )
                print(f"Created new collection: {self.collection_name}")
            
            # Load initial healthcare data if collection is empty
            await self._load_initial_data()
            
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise
    
    async def _load_initial_data(self):
        """Load initial healthcare documents if collection is empty"""
        try:
            count = self.collection.count()
            if count == 0:
                print("Loading initial healthcare documents...")
                await self._load_healthcare_datasets()
        except Exception as e:
            print(f"Error loading initial data: {e}")
    
    async def _load_healthcare_datasets(self):
        """Load healthcare datasets from various sources"""
        # Try to load from JSON file first
        try:
            import json
            import os
            json_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "healthcare_documents.json")
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    healthcare_docs = json.load(f)
                    await self.add_documents(healthcare_docs)
                    print(f"Loaded {len(healthcare_docs)} healthcare documents from JSON file")
                    return
        except Exception as e:
            print(f"Error loading from JSON file: {e}")
        
        # Fallback to hardcoded data
        healthcare_docs = [
            {
                "content": "Diabetes mellitus is a group of metabolic disorders characterized by high blood sugar levels over a prolonged period. Type 1 diabetes results from the pancreas's failure to produce enough insulin, while Type 2 diabetes begins with insulin resistance. Treatment includes lifestyle modifications, oral medications, and insulin therapy.",
                "metadata": {
                    "title": "Diabetes Overview",
                    "category": "Endocrinology",
                    "source": "Medical Textbook",
                    "keywords": ["diabetes", "insulin", "blood sugar", "metabolic"]
                }
            },
            {
                "content": "Hypertension, or high blood pressure, is a long-term medical condition in which the blood pressure in the arteries is persistently elevated. Normal blood pressure is typically less than 120/80 mmHg. Treatment includes lifestyle changes such as diet modification, exercise, and medications like ACE inhibitors, ARBs, or diuretics.",
                "metadata": {
                    "title": "Hypertension Management",
                    "category": "Cardiology",
                    "source": "Clinical Guidelines",
                    "keywords": ["hypertension", "blood pressure", "cardiovascular", "ACE inhibitors"]
                }
            },
            {
                "content": "COVID-19 is an infectious disease caused by the SARS-CoV-2 virus. Symptoms include fever, cough, fatigue, and loss of taste or smell. Severe cases can lead to pneumonia and acute respiratory distress syndrome. Prevention includes vaccination, mask-wearing, and social distancing.",
                "metadata": {
                    "title": "COVID-19 Information",
                    "category": "Infectious Diseases",
                    "source": "CDC Guidelines",
                    "keywords": ["COVID-19", "SARS-CoV-2", "pandemic", "vaccination"]
                }
            },
            {
                "content": "Heart disease refers to conditions that affect the heart's structure and function. Common types include coronary artery disease, heart failure, and arrhythmias. Risk factors include smoking, high cholesterol, diabetes, and family history. Prevention focuses on lifestyle modifications and regular screening.",
                "metadata": {
                    "title": "Heart Disease Prevention",
                    "category": "Cardiology",
                    "source": "American Heart Association",
                    "keywords": ["heart disease", "cardiovascular", "prevention", "risk factors"]
                }
            },
            {
                "content": "Mental health includes emotional, psychological, and social well-being. Common mental health conditions include depression, anxiety, bipolar disorder, and schizophrenia. Treatment options include therapy, medication, and lifestyle changes. Early intervention is crucial for better outcomes.",
                "metadata": {
                    "title": "Mental Health Overview",
                    "category": "Psychiatry",
                    "source": "Mental Health Foundation",
                    "keywords": ["mental health", "depression", "anxiety", "therapy"]
                }
            },
            {
                "content": "Pediatric care involves medical care for infants, children, and adolescents. Key areas include growth monitoring, vaccination schedules, developmental milestones, and age-appropriate treatments. Pediatricians must consider the unique physiological and psychological needs of young patients.",
                "metadata": {
                    "title": "Pediatric Care Principles",
                    "category": "Pediatrics",
                    "source": "American Academy of Pediatrics",
                    "keywords": ["pediatrics", "children", "vaccination", "development"]
                }
            },
            {
                "content": "Emergency medicine focuses on the immediate assessment and treatment of acute illnesses and injuries. Key principles include triage, rapid diagnosis, stabilization, and appropriate referral. Common emergencies include trauma, cardiac events, stroke, and respiratory distress.",
                "metadata": {
                    "title": "Emergency Medicine Basics",
                    "category": "Emergency Medicine",
                    "source": "Emergency Medicine Journal",
                    "keywords": ["emergency", "trauma", "triage", "acute care"]
                }
            },
            {
                "content": "Drug interactions occur when one medication affects the activity of another. Types include pharmacokinetic interactions (affecting drug absorption, distribution, metabolism, or excretion) and pharmacodynamic interactions (affecting drug action). Healthcare providers must review all medications to prevent adverse interactions.",
                "metadata": {
                    "title": "Drug Interactions",
                    "category": "Pharmacology",
                    "source": "Pharmacology Textbook",
                    "keywords": ["drug interactions", "pharmacokinetics", "medications", "adverse effects"]
                }
            }
        ]
        
        await self.add_documents(healthcare_docs)
        print(f"Loaded {len(healthcare_docs)} initial healthcare documents")
    
    async def add_documents(self, documents: List[Dict[str, Any]], collection_name: Optional[str] = None) -> int:
        """Add documents to the vector store"""
        try:
            if collection_name:
                try:
                    collection = self.client.get_collection(name=collection_name)
                except:
                    collection = self.client.create_collection(name=collection_name)
            else:
                collection = self.collection
            
            # Prepare documents for ingestion
            ids = []
            contents = []
            metadatas = []
            
            for doc in documents:
                doc_id = str(uuid.uuid4())
                ids.append(doc_id)
                contents.append(doc["content"])
                
                metadata = doc.get("metadata", {})
                metadata["created_at"] = datetime.now().isoformat()
                metadata["doc_id"] = doc_id
                
                # Convert list values to strings for ChromaDB compatibility
                for key, value in metadata.items():
                    if isinstance(value, list):
                        metadata[key] = ", ".join(str(item) for item in value)
                
                metadatas.append(metadata)
            
            # Add to collection
            collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas
            )
            
            return len(documents)
            
        except Exception as e:
            print(f"Error adding documents: {e}")
            raise
    
    async def search(self, query: str, limit: int = 5, threshold: float = 0.3) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                include=["documents", "metadatas", "distances"]
            )
            
            search_results = []
            for i, (doc, metadata, distance) in enumerate(zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )):
                # Convert distance to similarity score (ChromaDB uses cosine distance)
                # Handle cases where distance > 1 by using a different formula
                if distance <= 1:
                    similarity_score = 1 - distance
                else:
                    # For distances > 1, use a normalized similarity
                    similarity_score = max(0, 1 / (1 + distance))
                
                if similarity_score >= threshold:
                    search_results.append({
                        "document": {
                            "id": metadata.get("doc_id", f"doc_{i}"),
                            "content": doc,
                            "metadata": metadata,
                            "source": metadata.get("source", "Unknown"),
                            "created_at": metadata.get("created_at", datetime.now().isoformat())
                        },
                        "similarity_score": similarity_score,
                        "source": "vector_store"
                    })
            
            return search_results
            
        except Exception as e:
            print(f"Error searching vector store: {e}")
            raise
    
    async def get_collection_status(self) -> Dict[str, Any]:
        """Get status of the collection"""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "status": "active"
            }
        except Exception as e:
            return {
                "collection_name": self.collection_name,
                "document_count": 0,
                "status": "error",
                "error": str(e)
            }
    
    async def close(self):
        """Close the vector store connection"""
        if self.client:
            # ChromaDB client doesn't have an explicit close method
            pass
