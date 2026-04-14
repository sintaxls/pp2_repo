from __future__ import annotations

from pathlib import Path

import pygame


WINDOW_WIDTH = 850
WINDOW_HEIGHT = 500
FPS = 30
SUPPORTED_EXTENSIONS = {".mp3", ".wav"}


def load_playlist(music_dir: Path) -> list[Path]:
    playlist = sorted(
        path
        for path in music_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not playlist:
        raise FileNotFoundError(
            f"No supported audio files were found in {music_dir}"
        )
    return playlist


def measure_track_lengths(playlist: list[Path]) -> dict[Path, float]:
    lengths: dict[Path, float] = {}
    for track in playlist:
        try:
            lengths[track] = pygame.mixer.Sound(str(track)).get_length()
        except pygame.error:
            lengths[track] = 0.0
    return lengths


def play_track(playlist: list[Path], current_index: int) -> None:
    pygame.mixer.music.load(str(playlist[current_index]))
    pygame.mixer.music.play()


def stop_track() -> None:
    pygame.mixer.music.stop()


def get_current_position(is_playing: bool) -> float:
    if not is_playing:
        return 0.0

    position_ms = pygame.mixer.music.get_pos()
    if position_ms < 0:
        return 0.0
    return position_ms / 1000


def get_current_length(
    playlist: list[Path], current_index: int, track_lengths: dict[Path, float]
) -> float:
    return track_lengths.get(playlist[current_index], 0.0)


def format_seconds(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    minutes, remaining_seconds = divmod(total_seconds, 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"


def main() -> None:
    pygame.init()
    pygame.mixer.init()

    base_dir = Path(__file__).resolve().parent
    music_dir = base_dir / "music"
    playlist = load_playlist(music_dir)
    track_lengths = measure_track_lengths(playlist)
    current_index = 0
    is_playing = False
    stop_requested = False

    pygame.mixer.music.load(str(playlist[current_index]))

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Keyboard Music Player")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 28, bold=True)
    body_font = pygame.font.SysFont("arial", 22)
    small_font = pygame.font.SysFont("arial", 16)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    play_track(playlist, current_index)
                    is_playing = True
                    stop_requested = False
                elif event.key == pygame.K_s:
                    stop_track()
                    is_playing = False
                    stop_requested = True
                elif event.key == pygame.K_n:
                    current_index = (current_index + 1) % len(playlist)
                    play_track(playlist, current_index)
                    is_playing = True
                    stop_requested = False
                elif event.key == pygame.K_b:
                    current_index = (current_index - 1) % len(playlist)
                    play_track(playlist, current_index)
                    is_playing = True
                    stop_requested = False

        if is_playing and not pygame.mixer.music.get_busy():
            if stop_requested:
                stop_requested = False
            else:
                current_index = (current_index + 1) % len(playlist)
                play_track(playlist, current_index)

        current_track_name = playlist[current_index].stem
        current_position = get_current_position(is_playing)
        current_length = get_current_length(playlist, current_index, track_lengths)
        status = "Playing" if is_playing else "Stopped"

        screen.fill((255, 255, 255))

        screen.blit(title_font.render("Music Player", True, (0, 0, 0)), (30, 30))
        screen.blit(body_font.render(f"Status: {status}", True, (0, 0, 0)), (30, 80))
        screen.blit(body_font.render(f"Current Track: {current_track_name}", True, (0, 0, 0)), (30, 115),)
        screen.blit(small_font.render(f"Track {current_index + 1} of {len(playlist)}", True, (0, 0, 0),),(30, 150),)
        screen.blit(small_font.render(f"Position: {format_seconds(current_position)} / {format_seconds(current_length)}",True,(0, 0, 0),),(30, 185),)
        screen.blit(body_font.render("Controls", True, (0, 0, 0)), (30, 235))
        screen.blit(small_font.render("P = Play", True, (0, 0, 0)), (30, 270))
        screen.blit(small_font.render("S = Stop", True, (0, 0, 0)), (30, 300))
        screen.blit(small_font.render("N = Next track", True, (0, 0, 0)), (30, 330))
        screen.blit(small_font.render("B = Previous track", True, (0, 0, 0)), (230, 270))
        screen.blit(small_font.render("Q = Quit", True, (0, 0, 0)), (230, 300))

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
