# InfoTech Wizard - Frontend

A modern, responsive React-based chatbot interface for IT support assistance, built with TypeScript and Tailwind CSS. This frontend application provides an intuitive chat interface that communicates with the InfoTech Wizard backend API to deliver AI-powered IT support solutions.

## 🚀 Features

### Core Functionality
- **Real-time Chat Interface**: Interactive chat UI with smooth message rendering and auto-scroll
- **API Health Monitoring**: Real-time backend connectivity status with visual indicators
- **Message Processing Metrics**: Display processing time and context information for transparency
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Responsive Design**: Mobile-first responsive layout that works across all devices

### User Experience
- **Modern UI/UX**: Clean, gradient-based design with smooth animations and transitions
- **Loading States**: Visual feedback during message processing with animated indicators
- **Message History**: Persistent chat history during session
- **Context Display**: Shows which knowledge base context was used for responses
- **Accessibility**: Keyboard navigation support and semantic HTML structure

## 🛠️ Tech Stack

### Frontend Framework
- **React 18.3.1**: Modern React with hooks and functional components
- **TypeScript 5.5.3**: Full type safety and enhanced developer experience
- **Vite 5.4.2**: Fast build tool and development server with HMR

### Styling & UI
- **Tailwind CSS 3.4.1**: Utility-first CSS framework for rapid UI development
- **Lucide React 0.344.0**: Beautiful, customizable SVG icons
- **PostCSS 8.4.35**: CSS processing and optimization
- **Autoprefixer 10.4.18**: Automatic CSS vendor prefixing

### Development Tools
- **ESLint 9.9.1**: Code linting and quality enforcement
- **TypeScript ESLint**: TypeScript-specific linting rules
- **React Plugin**: React-specific ESLint rules and hooks validation

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── App.tsx            # Main application component
│   ├── main.tsx           # Application entry point
│   ├── index.css          # Global styles and Tailwind imports
│   └── vite-env.d.ts      # Vite environment types
├── index.html             # HTML template
├── package.json           # Dependencies and scripts
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
├── tsconfig.app.json      # App-specific TypeScript config
├── tsconfig.node.json     # Node-specific TypeScript config
├── eslint.config.js       # ESLint configuration
└── postcss.config.js      # PostCSS configuration
```

## 🔧 Configuration

### Backend Integration
The application is configured to communicate with the backend API:

- **API Endpoint**: `/api/v1/chat/` for chat interactions
- **Health Check**: `/health` for backend status monitoring
- **Proxy Configuration**: Vite development server proxies requests to `http://localhost:8000`

### API Request Format
```typescript
{
  query: string,      // User message
  top_k: 4,          // Number of context documents to retrieve
  max_tokens: 150    // Maximum response length
}
```

### API Response Format
```typescript
{
  response: string,         // AI-generated response
  context_used: string,     // Knowledge base context used
  processing_time: number,  // Response generation time in seconds
  query: string,           // Original user query
  timestamp: string        // Response timestamp
}
```

## 🚀 Getting Started

### Prerequisites
- **Node.js**: Version 18.0 or higher
- **npm**: Version 8.0 or higher
- **Backend API**: InfoTech Wizard backend running on port 8000

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   The application will start at `http://localhost:5173`

### Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build production-ready application |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint for code quality checks |

## 🔧 Development

### Environment Setup
The application uses Vite for development with the following features enabled:
- **Hot Module Replacement (HMR)**: Instant updates during development
- **TypeScript Support**: Full TypeScript compilation and type checking
- **CSS Processing**: Tailwind CSS compilation and optimization
- **Proxy Configuration**: API requests forwarded to backend server

### Code Style
- **TypeScript**: Strict mode enabled with comprehensive type checking
- **ESLint**: Enforced code quality and consistency rules
- **React Hooks**: Modern React patterns with functional components
- **CSS Classes**: Utility-first approach with Tailwind CSS

### Component Architecture
The application follows a simple, single-component architecture:

- **App.tsx**: Main component containing all chat functionality
- **State Management**: React hooks for local state management
- **API Integration**: Fetch API for backend communication
- **Type Safety**: Full TypeScript interfaces for all data structures

## 🌐 API Integration

### Chat Endpoint
- **URL**: `POST /api/v1/chat/`
- **Purpose**: Send user messages and receive AI responses
- **Response Time**: Tracked and displayed to users
- **Context**: Shows which knowledge base documents were used

### Health Check
- **URL**: `GET /health`
- **Purpose**: Monitor backend availability
- **Status Indicators**: Visual status in the header (Online/Offline/Checking)

### Error Handling
- Network errors are gracefully handled and displayed to users
- API errors show detailed error messages from the backend
- Connection status is continuously monitored

## 🎨 UI/UX Design

### Design System
- **Color Palette**: Blue and indigo gradient theme with gray accents
- **Typography**: System fonts with proper hierarchy and spacing
- **Icons**: Lucide React icons for consistent visual language
- **Animations**: Smooth transitions and loading states

### Responsive Design
- **Mobile-First**: Optimized for mobile devices with touch-friendly interfaces
- **Breakpoints**: Tailwind CSS responsive utilities for different screen sizes
- **Accessibility**: Proper contrast ratios and keyboard navigation support

### Chat Interface
- **Message Bubbles**: Distinct styling for user and AI messages
- **Timestamps**: Formatted time display for each message
- **Status Indicators**: Visual feedback for message status and processing
- **Auto-scroll**: Automatic scrolling to newest messages

## 🔐 Security Considerations

- **Input Sanitization**: User inputs are properly handled and sanitized
- **XSS Protection**: React's built-in XSS protection mechanisms
- **CORS Handling**: Proper cross-origin request handling via proxy
- **Error Information**: Error messages don't expose sensitive system information

## 📊 Performance

### Optimization Features
- **Code Splitting**: Vite's automatic code splitting for optimal loading
- **Tree Shaking**: Unused code elimination in production builds
- **Asset Optimization**: Automatic optimization of images and other assets
- **Lazy Loading**: Efficient resource loading strategies

### Bundle Analysis
- **Production Build**: Optimized and minified for production deployment
- **Source Maps**: Available for debugging in development
- **Modern JavaScript**: ES modules and modern JavaScript features

## 🚀 Deployment

### Production Build
```bash
npm run build
```
This creates an optimized production build in the `dist/` directory.

### Deployment Options
- **Static Hosting**: Can be deployed to any static hosting service
- **CDN**: Optimized for CDN distribution
- **Docker**: Can be containerized with a web server
- **Reverse Proxy**: Can be served behind a reverse proxy like Nginx

### Environment Variables
Configure backend API URL in `vite.config.ts` for different environments:
```typescript
server: {
  proxy: {
    '/api': {
      target: process.env.VITE_API_URL || 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Backend Connection Errors**
   - Verify backend is running on port 8000
   - Check proxy configuration in `vite.config.ts`
   - Ensure CORS is properly configured on backend

2. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
   - Check TypeScript configuration
   - Verify all dependencies are properly installed

3. **Development Server Issues**
   - Check port availability (default: 5173)
   - Clear Vite cache: `rm -rf node_modules/.vite`
   - Restart development server

### Performance Issues
- Check browser console for errors
- Verify network requests in browser DevTools
- Monitor backend response times
- Check for JavaScript errors that might block UI updates

## 🤝 Contributing

### Development Guidelines
1. Follow TypeScript best practices
2. Use Tailwind CSS utility classes
3. Maintain consistent code formatting with ESLint
4. Test on multiple screen sizes
5. Ensure accessibility standards are met

### Code Review Checklist
- [ ] TypeScript compilation passes without errors
- [ ] ESLint rules are followed
- [ ] Responsive design works on mobile and desktop
- [ ] Error handling is implemented
- [ ] Loading states are properly displayed

## 📝 License

This project is part of the InfoTech Wizard application suite. Please refer to the main project license for usage terms and conditions.

## 🆘 Support

For technical support or questions about the frontend implementation:
1. Check the troubleshooting section above
2. Review the backend API documentation
3. Check browser console for error messages
4. Verify backend connectivity and health status

---

*Built with ❤️ using React, TypeScript, and Tailwind CSS*