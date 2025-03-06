"""Command-line interface for the Twitter Thread Generator."""
import sys
from typing import List, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from ..thread_generator import ThreadGenerator, Thread

console = Console()

class CLI:
    """Command-line interface for managing Twitter threads."""
    
    def __init__(self):
        """Initialize the CLI interface."""
        self.generator = ThreadGenerator()
        
    def display_menu(self) -> str:
        """Display main menu and get user choice."""
        console.print(Panel.fit("Twitter Thread Generator", style="bold blue"))
        
        menu_items = [
            "1. Research and Generate Thread",
            "2. View Saved Threads",
            "3. Post Thread",
            "4. Exit"
        ]
        
        for item in menu_items:
            console.print(item)
            
        return Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4"])
    
    def research_and_generate(self):
        """Handle thread research and generation."""
        console.print("\n[bold]Research and Generate Thread[/bold]")
        
        topic = Prompt.ask("Enter topic to research")
        depth = Prompt.ask(
            "Select research depth",
            choices=["quick", "comprehensive"],
            default="comprehensive"
        )
        
        with console.status("Researching topic..."):
            try:
                thread = self.generator.research_and_generate(topic, depth)
            except Exception as e:
                console.print(f"[red]Error generating thread: {str(e)}[/red]")
                return
        
        # Display and save thread if generation was successful
        self.display_thread(thread)
        
        if Confirm.ask("Save this thread?"):
            try:
                self.generator.save_thread(thread)
                console.print("[green]Thread saved successfully![/green]")
            except Exception as e:
                console.print(f"[red]Error saving thread: {str(e)}[/red]")
    
    def view_saved_threads(self) -> Optional[Thread]:
        """Display saved threads and optionally select one."""
        console.print("\n[bold]Saved Threads[/bold]")
        
        try:
            threads = self.generator.load_threads()
            if not threads:
                console.print("[yellow]No saved threads found.[/yellow]")
                return None
            
            table = Table(show_header=True)
            table.add_column("#")
            table.add_column("Topic")
            table.add_column("Created")
            table.add_column("Status")
            
            for i, thread in enumerate(threads, 1):
                status = "Posted" if thread.tweet_ids else "Draft"
                table.add_row(
                    str(i),
                    thread.topic,
                    thread.created_at.strftime("%Y-%m-%d %H:%M"),
                    status
                )
            
            console.print(table)
            
            if Confirm.ask("View thread details?"):
                choice = int(Prompt.ask(
                    "Enter thread number",
                    choices=[str(i) for i in range(1, len(threads) + 1)]
                ))
                thread = threads[choice - 1]
                self.display_thread(thread)
                return thread
        except Exception as e:
            console.print(f"[red]Error loading threads: {str(e)}[/red]")
        
        return None
    
    def post_thread(self, thread: Optional[Thread] = None):
        """Post a thread to Twitter."""
        console.print("\n[bold]Post Thread to Twitter[/bold]")
        
        if not thread:
            try:
                threads = self.generator.load_threads()
                if not threads:
                    console.print("[yellow]No saved threads found.[/yellow]")
                    return
                
                # Display threads in a more compact format for posting
                table = Table(show_header=True)
                table.add_column("#", justify="right", style="cyan")
                table.add_column("Topic", style="green")
                table.add_column("Status", justify="center")
                
                for i, t in enumerate(threads, 1):
                    status = "[red]Posted[/red]" if t.tweet_ids else "[green]Draft[/green]"
                    table.add_row(str(i), t.topic, status)
                
                console.print(table)
                
                # Get thread selection
                choice = int(Prompt.ask(
                    "Select thread to post",
                    choices=[str(i) for i in range(1, len(threads) + 1)]
                ))
                thread = threads[choice - 1]
                
                # Show thread preview
                console.print("\n[bold]Thread Preview:[/bold]")
                self.display_thread(thread)
                
                if not Confirm.ask("\nPost this thread to Twitter?"):
                    return
                
                if thread.tweet_ids:
                    if not Confirm.ask("This thread has already been posted. Post again?"):
                        return
            except Exception as e:
                console.print(f"[red]Error loading threads: {str(e)}[/red]")
                return
        
        try:
            with console.status("[bold green]Posting thread to Twitter..."):
                thread = self.generator.post_thread(thread)
            
            console.print("\n[green]Thread posted successfully![/green]")
            console.print("\n[bold]Tweet URLs:[/bold]")
            for i, tweet_id in enumerate(thread.tweet_ids, 1):
                url = f"https://twitter.com/user/status/{tweet_id}"
                console.print(f"Tweet {i}: {url}")
            
            # Update saved thread
            self.generator.save_thread(thread)
        except Exception as e:
            console.print(f"[red]Error posting thread: {str(e)}[/red]")
    
    def display_thread(self, thread: Thread):
        """Display thread content."""
        console.print(f"\n[bold]Topic:[/bold] {thread.topic}")
        console.print("[bold]Tweets:[/bold]")
        
        for i, tweet in enumerate(thread.tweets, 1):
            console.print(f"\n[bold]Tweet {i}:[/bold]")
            console.print(Panel(tweet, width=70))
    
    def run(self):
        """Run the CLI interface."""
        while True:
            try:
                choice = self.display_menu()
                
                if choice == "1":
                    self.research_and_generate()
                elif choice == "2":
                    self.view_saved_threads()
                elif choice == "3":
                    self.post_thread()
                elif choice == "4":
                    console.print("[yellow]Goodbye![/yellow]")
                    sys.exit(0)
            except KeyboardInterrupt:
                console.print("\n[yellow]Operation cancelled.[/yellow]")
            except Exception as e:
                console.print(f"[red]An error occurred: {str(e)}[/red]")

def main():
    """Entry point for the CLI application."""
    CLI().run()

if __name__ == "__main__":
    main() 