# .NET Domain Knowledge

## Overview
.NET is a free, open-source, cross-platform framework for building modern applications. It supports multiple languages (primarily C# and F#) and runs on Windows, Linux, and macOS.

## Key Concepts
- **CLR (Common Language Runtime)**: Manages execution of .NET programs.
- **C#**: Primary language for .NET development, featuring strong typing and OOP.
- **NuGet**: Package manager for .NET libraries and tools.
- **ASP.NET Core**: Framework for building web applications and APIs.
- **Entity Framework**: ORM for database operations.
- **LINQ**: Language Integrated Query for data manipulation.

## Best Practices
- Use dependency injection for loosely coupled code.
- Implement proper exception handling and logging.
- Follow SOLID principles for maintainable architecture.
- Use async/await for non-blocking operations.
- Write unit tests with xUnit, NUnit, or MSTest.

## Example
```csharp
using System;

namespace HelloWorld
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, .NET!");
        }
    }
}

// ASP.NET Core controller example
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult GetUsers()
    {
        return Ok(new[] { "User1", "User2" });
    }
}
```