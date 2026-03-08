import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';

export async function POST(request: NextRequest) {
  try {
    const session = await getSession();

    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Receive multipart form data
    const formData = await request.formData();

    const context = formData.get('context') as string | null;
    const audioFile = formData.get('audio_file');

    if (!audioFile || !(audioFile instanceof File)) {
      return NextResponse.json(
        { error: 'audio_file is required and must be a file' },
        { status: 400 }
      );
    }

    const apiUrl = process.env.ML_AUDIO_ANALYZE_URL;

    if (!apiUrl) {
      console.error('[AUDIO_ANALYZE] ML API URL not configured');
      return NextResponse.json(
        { error: 'ML API not configured' },
        { status: 500 }
      );
    }

    console.log('[AUDIO_ANALYZE] Forwarding audio file to ML API:', apiUrl);
    console.log('[AUDIO_ANALYZE] File info:', {
      name: audioFile.name,
      size: audioFile.size,
      type: audioFile.type,
    });

    // Prepare FormData to send to ML server
    const forwardFormData = new FormData();
    forwardFormData.append('context', context || '');
    forwardFormData.append('audio_file', audioFile, audioFile.name || 'audio.wav');

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 120000);

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: forwardFormData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      const result = await response.json();

      if (!response.ok || result.status === 'error') {
        console.error('[AUDIO_ANALYZE] ML API Error:', result);

        return NextResponse.json(
          {
            error: 'ML API failed',
            details: result.message || 'Unknown error',
          },
          { status: response.status || 500 }
        );
      }

      return NextResponse.json({
        status: 'success',
        data: result.data,
      });

    } catch (fetchError: any) {
      clearTimeout(timeoutId);

      if (fetchError.name === 'AbortError') {
        console.error('[AUDIO_ANALYZE] ML API timeout');

        return NextResponse.json(
          {
            error: 'ML API timeout',
            details: 'Request exceeded 120 seconds',
          },
          { status: 504 }
        );
      }

      throw fetchError;
    }

  } catch (error: any) {
    console.error('[AUDIO_ANALYZE] Unexpected Error:', error);

    return NextResponse.json(
      {
        error: 'Failed to process audio analysis',
        details: error.message,
      },
      { status: 500 }
    );
  }
}