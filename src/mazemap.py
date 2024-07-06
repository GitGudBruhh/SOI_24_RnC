# Create map as string
# Can get map from files as string
# Made using asciiflow.com

maze = '''
                                          
                                          
     S────────────────────────────────────────────────────────────────────────────────────┐     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     │                                                                                    │     
     └────────────────────────────────────────────────────────────────────────────────────G     
                                          
                                          
                                          
'''

# Convert string to rows of strings for easier iteration and position access
maze_array = maze.split('\n')
