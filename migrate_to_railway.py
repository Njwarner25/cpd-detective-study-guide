#!/usr/bin/env python3
"""
Data migration script to import questions from local to Railway MongoDB
Run this script to populate the Railway database with questions
"""
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Railway MongoDB connection
RAILWAY_MONGO_URL = "mongodb://mongo:IvuXFcNBjbFHntwHJOQsJjuDOJXcMVFO@mongodb.railway.internal:27017"
RAILWAY_DB_NAME = "detective_study_guide"

async def import_data():
    # Connect to Railway MongoDB
    client = AsyncIOMotorClient(RAILWAY_MONGO_URL)
    db = client[RAILWAY_DB_NAME]
    
    print("Connected to Railway MongoDB")
    
    # Import collections
    collections_to_import = [
        ('questions', '/tmp/questions.json'),
        ('categories', '/tmp/categories.json'),
        ('users', '/tmp/users.json'),
    ]
    
    for collection_name, file_path in collections_to_import:
        print(f"\nImporting {collection_name}...")
        
        # Read JSON file
        with open(file_path, 'r') as f:
            # mongoexport creates one JSON object per line
            documents = [json.loads(line) for line in f if line.strip()]
        
        if documents:
            # Clear existing data
            await db[collection_name].delete_many({})
            print(f"  Cleared existing {collection_name}")
            
            # Insert new data
            result = await db[collection_name].insert_many(documents)
            print(f"  ✅ Imported {len(result.inserted_ids)} {collection_name}")
        else:
            print(f"  ⚠️  No data found in {file_path}")
    
    # Verify import
    print("\n=== Verification ===")
    print(f"Questions: {await db.questions.count_documents({})}")
    print(f"Categories: {await db.categories.count_documents({})}")
    print(f"Users: {await db.users.count_documents({})}")
    
    print("\n✅ Migration complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(import_data())
