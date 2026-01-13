# Ruby Domain Knowledge

## Overview
Ruby is a dynamic, open-source programming language focused on simplicity and productivity. It's known for its elegant syntax and is widely used for web development, particularly with the Ruby on Rails framework.

## Key Concepts
- **Object-Oriented**: Everything is an object, including primitives.
- **Dynamic Typing**: Variables don't require type declarations.
- **Blocks and Procs**: Anonymous functions for flexible code.
- **Gems**: Ruby packages managed by RubyGems.
- **Rails**: Full-stack web framework following MVC pattern.
- **Metaprogramming**: Code that writes code at runtime.

## Best Practices
- Follow Ruby style guidelines (use snake_case for methods/variables).
- Use meaningful variable and method names.
- Implement proper error handling with begin/rescue.
- Write tests with RSpec or Minitest.
- Use Bundler for dependency management.
- Leverage Ruby's DSL capabilities for domain-specific languages.

## Example
```ruby
# Basic Ruby syntax
def greet(name)
  "Hello, #{name}!"
end

puts greet("Ruby")

# Rails controller example
class UsersController < ApplicationController
  def index
    @users = User.all
    render json: @users
  end
  
  def create
    @user = User.new(user_params)
    if @user.save
      render json: @user, status: :created
    else
      render json: @user.errors, status: :unprocessable_entity
    end
  end
  
  private
  
  def user_params
    params.require(:user).permit(:name, :email)
  end
end
```