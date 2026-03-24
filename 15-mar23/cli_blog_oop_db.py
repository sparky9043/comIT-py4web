# blog_app.py

import sqlite3
from datetime import datetime
import os

class Database:
    """Handles all database operations for the blog"""
    
    def __init__(self, db_name="blog.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            # Enable foreign key constraints
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
    
    def create_tables(self):
        """Create the posts table if it doesn't exist"""
        try:
            # Create posts table with all required fields
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"❌ Error creating table: {e}")
    
    def add_post(self, title, author, content, timestamp):
        """Add a new post to the database"""
        try:
            self.cursor.execute('''
                INSERT INTO posts (title, author, content, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (title, author, content, timestamp))
            self.connection.commit()
            return self.cursor.lastrowid  # Return the ID of the new post
        except sqlite3.Error as e:
            print(f"❌ Error adding post: {e}")
            return None
    
    def get_all_posts(self):
        """Retrieve all posts from the database ordered by newest first"""
        try:
            self.cursor.execute('''
                SELECT id, title, author, content, timestamp 
                FROM posts 
                ORDER BY id DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error fetching posts: {e}")
            return []
    
    def get_post_by_id(self, post_id):
        """Retrieve a single post by its ID"""
        try:
            self.cursor.execute('''
                SELECT id, title, author, content, timestamp 
                FROM posts 
                WHERE id = ?
            ''', (post_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"❌ Error fetching post: {e}")
            return None
    
    def delete_post(self, post_id):
        """Delete a post from the database by ID"""
        try:
            self.cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0  # Return True if post was deleted
        except sqlite3.Error as e:
            print(f"❌ Error deleting post: {e}")
            return False
    
    def search_posts_by_title(self, keyword):
        """Search posts by title (case-insensitive)"""
        try:
            self.cursor.execute('''
                SELECT id, title, author, content, timestamp 
                FROM posts 
                WHERE title LIKE ? 
                ORDER BY id DESC
            ''', (f'%{keyword}%',))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error searching posts: {e}")
            return []
    
    def search_posts_by_content(self, keyword):
        """Search posts by content (case-insensitive)"""
        try:
            self.cursor.execute('''
                SELECT id, title, author, content, timestamp 
                FROM posts 
                WHERE content LIKE ? 
                ORDER BY id DESC
            ''', (f'%{keyword}%',))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error searching posts: {e}")
            return []
    
    def search_posts_by_title_or_content(self, keyword):
        """Search posts by title OR content (case-insensitive)"""
        try:
            self.cursor.execute('''
                SELECT id, title, author, content, timestamp 
                FROM posts 
                WHERE title LIKE ? OR content LIKE ? 
                ORDER BY id DESC
            ''', (f'%{keyword}%', f'%{keyword}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"❌ Error searching posts: {e}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()


class Post:
    """Represents a single blog post"""
    
    def __init__(self, post_id, title, author, content, timestamp):
        """Initialize a post with data from database"""
        self.id = post_id  # Database ID
        self.title = title
        self.author = author
        self.content = content
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S') if isinstance(timestamp, str) else timestamp
        
    def display(self):
        """Display the post in a formatted way"""
        print("\n" + "="*50)
        print(f"📝 #{self.id}: {self.title}")
        print("="*50)
        print(f"✍️  Author: {self.author}")
        print(f"🕐 Posted on: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*50)
        print(f"{self.content}")
        print("="*50 + "\n")
    
    def get_short_info(self):
        """Return a short summary of the post"""
        date_str = self.timestamp.strftime('%Y-%m-%d')
        return f"📌 [#{self.id}] {self.title} | {self.author} | {date_str}"


class Blog:
    """Represents the entire blog with database integration"""
    
    def __init__(self, name):
        """Initialize the blog with a name and database connection"""
        self.name = name
        self.db = Database()  # Create database handler
        
    def add_post(self, title, author, content):
        """Add a new post to the database"""
        # Get current timestamp as string for database storage
        current_time = datetime.now()
        timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Add to database
        post_id = self.db.add_post(title, author, content, timestamp_str)
        
        if post_id:
            print(f"\n✅ Post '{title}' added successfully! (ID: {post_id})")
            return post_id
        else:
            print(f"\n❌ Failed to add post '{title}'")
            return None
    
    def view_all_posts(self):
        """Display all posts from the database"""
        posts_data = self.db.get_all_posts()
        
        if not posts_data:
            print("\n📭 No posts yet. Start by adding a post!")
            return
        
        print(f"\n📚 {self.name} - All Posts ({len(posts_data)} total)")
        print("="*50)
        
        # Convert database records to Post objects and display
        for post_data in posts_data:
            post = Post(*post_data)  # Unpack tuple into Post constructor
            print(post.get_short_info())
        
        print("="*50)
    
    def view_post_details(self, post_id):
        """View a specific post by its ID"""
        post_data = self.db.get_post_by_id(post_id)
        
        if post_data:
            post = Post(*post_data)
            post.display()
        else:
            print(f"\n❌ Post with ID #{post_id} not found!")
    
    def delete_post(self, post_id):
        """Delete a post by its ID"""
        # First check if post exists
        post_data = self.db.get_post_by_id(post_id)
        
        if post_data:
            post = Post(*post_data)
            if self.db.delete_post(post_id):
                print(f"\n✅ Post '{post.title}' (ID: {post_id}) deleted successfully!")
            else:
                print(f"\n❌ Failed to delete post ID #{post_id}")
        else:
            print(f"\n❌ Post with ID #{post_id} not found!")
    
    def search_posts(self, keyword, search_type="all"):
        """
        Search posts with different search types:
        - "title": search only in titles
        - "content": search only in content
        - "all": search in both title and content
        """
        if not keyword:
            print("\n❌ Please enter a keyword to search!")
            return []
        
        # Perform search based on type
        if search_type == "title":
            results = self.db.search_posts_by_title(keyword)
            search_desc = f"titles containing '{keyword}'"
        elif search_type == "content":
            results = self.db.search_posts_by_content(keyword)
            search_desc = f"content containing '{keyword}'"
        else:  # "all"
            results = self.db.search_posts_by_title_or_content(keyword)
            search_desc = f"titles or content containing '{keyword}'"
        
        if results:
            print(f"\n🔍 Found {len(results)} post(s) with {search_desc}:")
            print("-"*40)
            for post_data in results:
                post = Post(*post_data)
                print(post.get_short_info())
                # Show a snippet of content for content searches
                if search_type in ["content", "all"] and len(post.content) > 100:
                    print(f"   📄 Snippet: {post.content[:100]}...")
                elif search_type in ["content", "all"]:
                    print(f"   📄 Snippet: {post.content}")
                print()
        else:
            print(f"\n🔍 No posts found with {search_desc}")
        
        return results
    
    def get_post_count(self):
        """Get total number of posts in database"""
        return len(self.db.get_all_posts())
    
    def close(self):
        """Close database connection"""
        self.db.close()


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the blog application header"""
    print("╔══════════════════════════════════════════╗")
    print("║     📝 TERMINAL BLOG APP (SQLite)        ║")
    print("╚══════════════════════════════════════════╝")


def print_post_input_instructions():
    """Print instructions for entering post content"""
    print("\n✏️  CREATE A NEW POST")
    print("-"*30)
    print("📝 Instructions:")
    print("   - Enter your content line by line")
    print("   - Press Enter twice to finish\n")


def main():
    """Main function to run the blog application"""
    
    # Get blog name from user
    blog_name = input("Enter your blog name: ").strip()
    if not blog_name:
        blog_name = "My Awesome Blog"
    
    # Create blog instance (this automatically creates/connects to database)
    my_blog = Blog(blog_name)
    
    while True:
        clear_screen()
        print_header()
        print(f"\n🌟 Welcome to '{my_blog.name}'!")
        print(f"📊 Total posts: {my_blog.get_post_count()}")
        print("\n📋 MENU OPTIONS:")
        print("1. ✏️  Add a new post")
        print("2. 📖 View all posts")
        print("3. 🔍 View a specific post (by ID)")
        print("4. 🗑️  Delete a post (by ID)")
        print("5. 🔎 Search posts")
        print("6. 🚪 Exit")
        
        choice = input("\n👉 Choose an option (1-6): ").strip()
        
        if choice == '1':
            # Add a new post
            clear_screen()
            print_header()
            print_post_input_instructions()
            
            title = input("📌 Post title: ").strip()
            if not title:
                print("\n❌ Title cannot be empty!")
                input("\nPress Enter to continue...")
                continue
                
            author = input("✍️  Author name: ").strip()
            if not author:
                author = "Anonymous"
            
            print("\n📝 Enter your content:")
            print("-"*30)
            content_lines = []
            empty_lines = 0
            
            while True:
                line = input()
                if line == "":
                    empty_lines += 1
                    if empty_lines == 2:  # Two consecutive empty lines to finish
                        break
                else:
                    empty_lines = 0
                    content_lines.append(line)
            
            content = "\n".join(content_lines).strip()
            if not content:
                print("\n❌ Content cannot be empty!")
                input("\nPress Enter to continue...")
                continue
            
            # Add post to database
            my_blog.add_post(title, author, content)
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            # View all posts
            clear_screen()
            print_header()
            my_blog.view_all_posts()
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            # View a specific post
            clear_screen()
            print_header()
            my_blog.view_all_posts()
            
            if my_blog.get_post_count() > 0:
                try:
                    post_id = int(input("\n🔍 Enter post ID to view: "))
                    my_blog.view_post_details(post_id)
                except ValueError:
                    print("\n❌ Please enter a valid number!")
            
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            # Delete a post
            clear_screen()
            print_header()
            my_blog.view_all_posts()
            
            if my_blog.get_post_count() > 0:
                try:
                    post_id = int(input("\n🗑️  Enter post ID to delete: "))
                    # Double-check post exists
                    post_data = my_blog.db.get_post_by_id(post_id)
                    if post_data:
                        post = Post(*post_data)
                        confirm = input(f"Are you sure you want to delete '{post.title}'? (y/n): ")
                        if confirm.lower() == 'y':
                            my_blog.delete_post(post_id)
                        else:
                            print("\n❌ Deletion cancelled.")
                    else:
                        print(f"\n❌ Post with ID #{post_id} not found!")
                except ValueError:
                    print("\n❌ Please enter a valid number!")
            
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            # Search posts
            clear_screen()
            print_header()
            print("🔎 SEARCH OPTIONS:")
            print("1. Search by title only")
            print("2. Search by content only")
            print("3. Search by title OR content")
            
            search_choice = input("\nChoose search type (1-3): ").strip()
            
            keyword = input("Enter search keyword: ").strip()
            
            if keyword:
                if search_choice == '1':
                    my_blog.search_posts(keyword, "title")
                elif search_choice == '2':
                    my_blog.search_posts(keyword, "content")
                elif search_choice == '3':
                    my_blog.search_posts(keyword, "all")
                else:
                    print("\n❌ Invalid search option! Using default (title OR content)")
                    my_blog.search_posts(keyword, "all")
            else:
                print("\n❌ Please enter a keyword to search!")
            
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            # Exit
            clear_screen()
            print_header()
            print(f"\n👋 Thanks for using '{my_blog.name}'!")
            print(f"📊 Total posts saved: {my_blog.get_post_count()}")
            print("💾 Data has been saved to database!")
            print("Goodbye!")
            my_blog.close()  # Close database connection
            break
        
        else:
            print("\n❌ Invalid choice! Please enter 1-6.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()